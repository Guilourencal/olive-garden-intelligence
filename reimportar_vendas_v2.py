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

ARQUIVO = r'data/Vendas_Geral/DASH VENDAS 2026 _ 12.05 corrigido 2.xlsx'

print('Lendo arquivo...')
df = pd.read_excel(ARQUIVO, sheet_name='Dados', header=0)
df['data'] = pd.to_datetime(df['dia'], errors='coerce')
df = df[df['data'].notna() & df['restaurante'].notna()].copy()
df = df[df['ANO'] >= 2025].copy()
print(f'Linhas 2025+: {len(df)}')
print(f'Range: {df["data"].min().date()} a {df["data"].max().date()}')
print(f'Anos: {sorted(df["ANO"].unique())}')
print(f'Filiais: {sorted(df["restaurante"].unique())}')
print('\nProsseguir com reimport? (s/n)')
resp = input()
if resp.lower() != 's':
    print('Cancelado.')
    exit()

conn = get_conn()
cur = conn.cursor()

cur.execute('DELETE FROM vendas_diarias')
print(f'Registros removidos do banco: {cur.rowcount}')
conn.commit()

def safe_float(v):
    if pd.isna(v): return None
    try: return float(str(v).replace(',','.').replace('\t','').strip())
    except: return None

def safe_int(v):
    f = safe_float(v)
    return int(f) if f is not None else None

ins = err = skip = 0
for _, row in df.iterrows():
    try:
        filial = MAPA_FILIAIS.get(str(row['restaurante']).strip())
        if not filial:
            skip += 1
            continue
        data = row['data'].date()
        cur.execute("""
            INSERT INTO vendas_diarias (
                data, filial, ano, mes, dia_semana, semana,
                venda_salao, gc_salao, venda_dlv, gc_dlv,
                venda_total, meta_venda, venda_ano1,
                ticket_total, pct_salao, pct_dlv, pct_togo,
                hdc, venda_por_hdc
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (data, filial) DO UPDATE SET
                venda_salao=EXCLUDED.venda_salao,
                gc_salao=EXCLUDED.gc_salao,
                venda_dlv=EXCLUDED.venda_dlv,
                gc_dlv=EXCLUDED.gc_dlv,
                venda_total=EXCLUDED.venda_total,
                meta_venda=EXCLUDED.meta_venda,
                venda_ano1=EXCLUDED.venda_ano1,
                ticket_total=EXCLUDED.ticket_total,
                pct_salao=EXCLUDED.pct_salao,
                pct_dlv=EXCLUDED.pct_dlv,
                pct_togo=EXCLUDED.pct_togo,
                hdc=EXCLUDED.hdc,
                venda_por_hdc=EXCLUDED.venda_por_hdc
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
            safe_float(row.get('SALAO (%)', row.get('SALÃO (%)'))),
            safe_float(row.get('DLV (%)')),
            safe_float(row.get('TOGO (%)')),
            safe_int(row.get('HDC ATUAL')),
            safe_float(row.get('VENDA POR HDC')),
        ))
        ins += 1
    except Exception as e:
        conn.rollback()
        err += 1
        if err <= 5: print(f'  Erro linha {_}: {e}')

conn.commit()
print(f'\nInseridos/Atualizados: {ins} | Skips: {skip} | Erros: {err}')

cur.execute('SELECT filial, COUNT(id), MIN(data), MAX(data) FROM vendas_diarias GROUP BY filial ORDER BY filial')
print('\nResumo banco:')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]} dias | {row[2]} a {row[3]}')

cur.close()
conn.close()
print('Concluido!')
