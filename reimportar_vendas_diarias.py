import pandas as pd
from db import get_conn
import psycopg2

MAPA_FILIAIS = {
    'MOR': 'Olive Garden - Morumbi',
    'CNO': 'Olive Garden - Center Norte',
    'ARI': 'Olive Garden - Aricanduva',
    'DPO': 'Olive Garden - Dom Pedro',
    'GRU2': 'Olive Garden - Guarulhos GRU2',
    'GRU3': 'Olive Garden - Guarulhos GRU3',
}

print('Lendo arquivo...')
df = pd.read_excel('data/dash_vendas.xlsx', sheet_name='Dados', header=0, nrows=10000)
df['data'] = pd.to_datetime(df['dia'], errors='coerce')
df = df[df['data'].notna() & df['restaurante'].notna()].copy()
df = df[df['ANO'] >= 2025].copy()
print(f'Linhas 2025+: {len(df)}')
print(f'Range: {df["data"].min()} a {df["data"].max()}')
print(f'Anos: {sorted(df["ANO"].unique())}')

conn = get_conn()
cur = conn.cursor()

# Limpar dados existentes e reimportar
cur.execute('DELETE FROM vendas_diarias')
print(f'Registros removidos: {cur.rowcount}')
conn.commit()

ins = err = 0
for _, row in df.iterrows():
    try:
        filial = MAPA_FILIAIS.get(str(row['restaurante']).strip(), str(row['restaurante']))
        data = row['data'].date()
        
        def safe_float(v):
            if pd.isna(v): return None
            try: return float(str(v).replace(',','.').replace('\t','').strip())
            except: return None
        
        def safe_int(v):
            f = safe_float(v)
            return int(f) if f is not None else None

        cur.execute("""
            INSERT INTO vendas_diarias (
                data, filial, ano, mes, dia_semana, semana,
                venda_salao, gc_salao, venda_dlv, gc_dlv,
                venda_total, meta_venda, venda_ano1,
                ticket_total, pct_salao, pct_dlv, pct_togo,
                hdc, venda_por_hdc
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (data, filial) DO NOTHING
        """, (
            data, filial,
            safe_int(row.get('ANO')),
            str(row['MÊS']) if pd.notna(row.get('MÊS')) else None,
            str(row['dia semana']) if pd.notna(row.get('dia semana')) else None,
            str(row['SEMANA']) if pd.notna(row.get('SEMANA')) else None,
            safe_float(row.get('D.ROOM')),
            safe_int(row.get("gc´s DR")),
            safe_float(row.get('DLV')),
            safe_int(row.get("TCs\nDLV")),
            safe_float(row.get('VENDA TOTAL')),
            safe_float(row.get('META VENDA R$')),
            safe_float(row.get('VENDA ANO-1')),
            safe_float(row.get('TICKET TOTAL')),
            safe_float(row.get('SALÃO (%)')),
            safe_float(row.get('DLV (%)')),
            safe_float(row.get('TOGO (%)')),
            safe_int(row.get('HDC ATUAL')),
            safe_float(row.get('VENDA POR HDC')),
        ))
        if cur.rowcount > 0: ins += 1
    except Exception as e:
        conn.rollback()
        err += 1
        if err <= 3: print(f'  Erro: {e}')

conn.commit()
cur.execute('SELECT filial, COUNT(id), MIN(data), MAX(data) FROM vendas_diarias GROUP BY filial ORDER BY filial')
print('\nResumo:')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]} dias | {row[2]} a {row[3]}')
print(f'\nInseridos: {ins} | Erros: {err}')
cur.close()
conn.close()
print('Concluido!')
