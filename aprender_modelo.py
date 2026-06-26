import psycopg2
from db import get_conn
import pandas as pd
import numpy as np
from datetime import date, timedelta

def calcular_modelo_filial(dff, hoje, datas_eventos=set()):
    dff = dff[(dff["venda_salao"] > 0) & (~dff["data"].dt.date.isin(datas_eventos))].copy()
    dff['dow'] = dff['data'].dt.dayofweek
    dff['mes'] = dff['data'].dt.month

    # Remover outliers por DOW
    clean_parts = []
    for dow_v in dff['dow'].unique():
        grupo = dff[dff['dow'] == dow_v]
        q1 = grupo['venda_salao'].quantile(0.10)
        q3 = grupo['venda_salao'].quantile(0.90)
        iqr = q3 - q1
        clean_parts.append(grupo[(grupo['venda_salao'] >= q1-1.5*iqr) & (grupo['venda_salao'] <= q3+1.5*iqr)])
    dff_c = pd.concat(clean_parts)

    media = dff_c['venda_salao'].mean()
    fator_dow = dff_c.groupby('dow')['venda_salao'].mean() / media
    fator_mes = dff_c.groupby('mes')['venda_salao'].mean() / media
    # Fator semana do mes (S1=dias 1-7, S2=8-14, S3=15-21, S4=22-31)
    dff_c['semana_mes'] = dff_c['data'].dt.day.apply(lambda d: 1 if d<=7 else 2 if d<=14 else 3 if d<=21 else 4)
    fator_semana_mes = dff_c.groupby('semana_mes')['venda_salao'].mean() / media
    recente = dff_c[dff_c['data'] >= hoje - timedelta(days=28)]
    fator_rec_raw = recente['venda_salao'].mean() / media if len(recente) > 0 else 1.0
    fator_rec = float(np.clip(fator_rec_raw, 0.85, 1.15))
    fator_a1 = (dff_c['venda_salao'] / dff['venda_ano1']).replace([np.inf,-np.inf], np.nan).dropna().median()

    # Pesos automaticos por backtest 3 janelas
    mapes_stl, mapes_a1 = [], []
    for janela in [56, 84, 112]:
        corte = hoje - timedelta(days=janela)
        treino = dff_c[dff_c['data'] <= corte]
        teste = dff[(dff['data'] > corte) & (dff['data'] <= corte + timedelta(days=28))]
        if len(treino) < 30 or len(teste) == 0:
            continue
        m_b = treino['venda_salao'].mean()
        f_d = treino.groupby('dow')['venda_salao'].mean() / m_b
        f_m = treino.groupby('mes')['venda_salao'].mean() / m_b
        rec_t = treino[treino['data'] >= corte - timedelta(days=28)]
        f_r = float(np.clip(rec_t['venda_salao'].mean() / m_b if len(rec_t) > 0 else 1.0, 0.85, 1.15))
        f_a = (treino['venda_salao'] / dff[dff['data'] <= corte]['venda_ano1']).replace([np.inf,-np.inf], np.nan).dropna().median()
        e_stl, e_a1 = [], []
        for _, row in teste.iterrows():
            p_s = m_b * f_d.get(row['dow'],1.0) * f_m.get(row['mes'],1.0) * f_r
            real = row['venda_salao']
            e_stl.append(abs(p_s - real) / real * 100)
            if pd.notna(row['venda_ano1']) and row['venda_ano1'] > 0:
                e_a1.append(abs(row['venda_ano1'] * f_a - real) / real * 100)
        if e_stl: mapes_stl.append(np.mean(e_stl))
        if e_a1: mapes_a1.append(np.mean(e_a1))

    if mapes_stl and mapes_a1:
        inv_stl = 1 / np.mean(mapes_stl)
        inv_a1 = 1 / np.mean(mapes_a1)
        peso_stl = inv_stl / (inv_stl + inv_a1)
    else:
        peso_stl = 0.7
    peso_a1 = 1 - peso_stl

    return {
        'media': media, 'fator_dow': fator_dow, 'fator_mes': fator_mes, 'fator_semana_mes': fator_semana_mes,
        'fator_rec': fator_rec, 'fator_a1': fator_a1,
        'peso_stl': peso_stl, 'peso_a1': peso_a1
    }

print('=== SISTEMA DE APRENDIZADO CONTINUO ===')
print()

conn = get_conn()
df = pd.read_sql('SELECT data, filial, venda_salao, venda_ano1 FROM vendas_diarias ORDER BY data', conn)
conn.close()

df['data'] = pd.to_datetime(df['data'])
df['filial_curta'] = df['filial'].str.replace('Olive Garden - ', '', regex=False)
df['dow'] = df['data'].dt.dayofweek
df['mes'] = df['data'].dt.month

hoje = df['data'].max()
inicio_proj = hoje + timedelta(days=1)

# ETAPA 1 — Atualizar erros de projecoes passadas
print('ETAPA 1 — Calculando erros de projecoes passadas...')
conn = get_conn()
cur = conn.cursor()

cur.execute('SELECT id, filial, data_alvo, valor_projetado FROM projecoes_historico WHERE valor_realizado IS NULL AND data_alvo <= %s', (hoje.date(),))
pendentes = cur.fetchall()
atualizados = 0
for pid, filial, data_alvo, proj in pendentes:
    filial_full = 'Olive Garden - ' + filial if not filial.startswith('Olive') else filial
    real_row = df[(df['filial'] == filial_full) & (df['data'].dt.date == data_alvo)]
    if len(real_row) > 0:
        real = float(real_row["venda_salao"].values[0])
        erro_abs = float(abs(proj - real))
        erro_pct = float((proj - real) / real * 100) if real > 0 else None
        cur.execute('UPDATE projecoes_historico SET valor_realizado=%s, erro_absoluto=%s, erro_pct=%s WHERE id=%s',
                   (real, erro_abs, erro_pct, pid))
        atualizados += 1
conn.commit()
print(f'  {atualizados} projecoes atualizadas com valores realizados')

# ETAPA 2 — Gerar e salvar projecoes para os proximos 28 dias
print('ETAPA 2 — Gerando projecoes para proximos 28 dias...')
inseridos = 0
# Carregar datas de eventos por filial
conn_ev = get_conn()
cur_ev = conn_ev.cursor()
cur_ev.execute("SELECT filial, data_inicio, data_fim FROM calendario_eventos")
eventos_db = cur_ev.fetchall()
cur_ev.close()
conn_ev.close()
from datetime import date as _date
eventos_por_filial = {}
for fil_ev, d_ini, d_fim in eventos_db:
    fil_curta = fil_ev.replace("Olive Garden - ", "") if fil_ev else None
    d = d_ini
    while d <= d_fim:
        if fil_curta:
            eventos_por_filial.setdefault(fil_curta, set()).add(d)
        else:
            for _f in ['Aricanduva','Center Norte','Dom Pedro','Guarulhos GRU2','Guarulhos GRU3','Morumbi']:
                eventos_por_filial.setdefault(_f, set()).add(d)
        d = _date(d.year, d.month, d.day + 1) if d.day < 28 else (_date(d.year, d.month+1, 1) if d.month < 12 else _date(d.year+1, 1, 1))

for filial in sorted(df['filial_curta'].unique()):
    dff = df[df['filial_curta'] == filial].copy().sort_values('data')
    if len(dff) < 60:
        continue
    m = calcular_modelo_filial(dff, hoje, eventos_por_filial.get(filial, set()))
    filial_full = 'Olive Garden - ' + filial

    for d in range(1, 29):
        data_alvo = inicio_proj + timedelta(days=d-1)
        dow_d = data_alvo.weekday()
        mes_d = data_alvo.month
        sem_d = 1 if data_alvo.day<=7 else 2 if data_alvo.day<=14 else 3 if data_alvo.day<=21 else 4
        f_sem = float(m['fator_semana_mes'].get(sem_d, 1.0))
        p_stl = m['media'] * m['fator_dow'].get(dow_d,1.0) * m['fator_mes'].get(mes_d,1.0) * m['fator_rec'] * f_sem
        data_ano1 = data_alvo - timedelta(days=364)
        ano1_row = dff[dff['data'].dt.date == data_ano1.date()]
        if len(ano1_row) > 0 and ano1_row['venda_salao'].values[0] > 0:
            p_a1 = ano1_row['venda_salao'].values[0] * m['fator_a1']
            p_final = p_stl * m['peso_stl'] + p_a1 * m['peso_a1']
        else:
            p_final = p_stl
        try:
            sql_ins = "INSERT INTO projecoes_historico (data_projecao, filial, data_alvo, valor_projetado, fator_dow, fator_mes, fator_rec, peso_stl, peso_a1) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (data_projecao, filial, data_alvo) DO NOTHING"
            cur.execute(sql_ins, (hoje.date(), filial, data_alvo.date(), float(max(p_final,0)),
                float(m["fator_dow"].get(dow_d,1.0)), float(m["fator_mes"].get(mes_d,1.0)),
                float(m["fator_rec"]), float(m["peso_stl"]), float(m["peso_a1"])))
            if cur.rowcount > 0: inseridos += 1
            if cur.rowcount > 0: inseridos += 1
        except Exception as e:
            conn.rollback()
print(f'  {inseridos} projecoes salvas para os proximos 28 dias')

# ETAPA 3 — Recalibrar parametros com base no historico de erros
print('ETAPA 3 — Recalibrando parametros do modelo...')
sql_stats = "SELECT filial, AVG(ABS(erro_pct)) as mape, AVG(erro_pct) as bias, COUNT(*) as n FROM projecoes_historico WHERE valor_realizado IS NOT NULL AND erro_pct IS NOT NULL GROUP BY filial ORDER BY filial"
cur.execute(sql_stats)
stats = cur.fetchall()
for filial, mape, bias, n in stats:
    sql = "INSERT INTO modelo_parametros (filial, parametro, valor, amostras, mape_historico, bias_historico) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (filial, parametro) DO UPDATE SET valor=EXCLUDED.valor, amostras=EXCLUDED.amostras, mape_historico=EXCLUDED.mape_historico, bias_historico=EXCLUDED.bias_historico, atualizado_em=CURRENT_TIMESTAMP"
    cur.execute(sql, (filial, "mape_bias", float(mape) if mape else 0, int(n), float(mape) if mape else 0, float(bias) if bias else 0))
    if mape and bias:
        print(f'  {filial}: MAPE={mape:.1f}% | Bias={bias:+.1f}% | n={n}')
conn.commit()
cur.close()
conn.close()
print()
print('Aprendizado concluido!')
