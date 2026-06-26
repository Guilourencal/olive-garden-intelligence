import psycopg2
from db import get_conn
import pandas as pd
import numpy as np
from datetime import date, timedelta

conn = get_conn()

# Vendas ultimas 8 semanas vs ano anterior
df_vd = pd.read_sql('SELECT data, filial, venda_salao, venda_ano1 FROM vendas_diarias ORDER BY data', conn)

# GSS ultimo periodo
df_gss = pd.read_sql("""
    SELECT restaurant, periodo, overall_experience
    FROM pesquisa_performance
    ORDER BY periodo DESC
""", conn)

# Reviews sentimento
df_rev = pd.read_sql("""
    SELECT filial, sentimento, nota
    FROM reviews
    WHERE plataforma != 'iFood'
""", conn)

conn.close()

df_vd['data'] = pd.to_datetime(df_vd['data'])
hoje = df_vd['data'].max()

print('=== SCORE PREDITIVO DE RISCO ===')
print(f'Data referencia: {hoje.date()}')
print(f'Ultimo periodo GSS: {df_gss["periodo"].iloc[0]}')
print()

for filial in sorted(df_vd['filial'].unique()):
    filial_c = filial.replace('Olive Garden - ','')
    
    # Tendencia de vendas — ultimas 8 semanas vs ano anterior
    df_f = df_vd[df_vd['filial']==filial].copy()
    ult8 = df_f[df_f['data'] >= hoje - timedelta(days=56)]
    media_rec = ult8['venda_salao'].mean()
    media_aa = ult8['venda_ano1'].mean()
    delta_venda = (media_rec / media_aa - 1) * 100 if media_aa > 0 else 0
    score_venda = max(0, -delta_venda) * 2 if delta_venda < -5 else 0

    # GSS
    filial_gss_map = {
        'Aricanduva': 'Olive Garden - Aricanduva',
        'Center Norte': 'Olive Garden - Center Norte',
        'Dom Pedro': 'Olive Garden - Dom Pedro',
        'Guarulhos GRU2': 'Olive Garden - Guarulhos GRU2',
        'Guarulhos GRU3': 'Olive Garden - Guarulhos GRU3',
        'Morumbi': 'Olive Garden - Morumbi',
    }
    gss_ult = df_gss[df_gss['restaurant']==filial].head(1)
    gss_val = gss_ult['overall_experience'].values[0] if len(gss_ult) > 0 else 90
    score_gss = max(0, (90 - gss_val)) * 1.5 if gss_val < 90 else 0

    # Reputacao publica
    df_rev_f = df_rev[df_rev['filial']==filial]
    pct_pos = len(df_rev_f[df_rev_f['sentimento']=='Positivo']) / len(df_rev_f) * 100 if len(df_rev_f) > 0 else 70
    score_rep = max(0, (70 - pct_pos)) * 1.0 if pct_pos < 70 else 0

    score_total = score_venda * 0.5 + score_gss * 0.3 + score_rep * 0.2
    nivel = 'ALTO' if score_total > 25 else 'MEDIO' if score_total > 12 else 'BAIXO'

    print(f'{filial_c}:')
    print(f'  Tendencia vendas: {delta_venda:+.1f}% | score_venda={score_venda:.1f}')
    print(f'  GSS: {gss_val:.1f}% | score_gss={score_gss:.1f}')
    print(f'  Reputacao: {pct_pos:.1f}% pos | score_rep={score_rep:.1f}')
    print(f'  SCORE TOTAL: {score_total:.1f} → {nivel}')
    print()
