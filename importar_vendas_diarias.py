import pandas as pd
from db import get_conn
import psycopg2
from datetime import datetime

MAPA_FILIAIS = {
    'MOR': 'Olive Garden - Morumbi',
    'CNO': 'Olive Garden - Center Norte',
    'ARI': 'Olive Garden - Aricanduva',
    'DPO': 'Olive Garden - Dom Pedro',
    'GRU2': 'Olive Garden - Guarulhos GRU2',
    'GRU3': 'Olive Garden - Guarulhos GRU3',
}

print('Lendo arquivo...')
df = pd.read_excel('data/dash_vendas.xlsx', sheet_name='Dados', header=0)
print(f'Total de linhas: {len(df)}')

# Filtrar apenas 2025 em diante
df = df[pd.to_datetime(df['dia'], errors='coerce') >= '2025-01-01'].copy()
df = df[df['restaurante'].notna() & df['dia'].notna()].copy()
df['data'] = pd.to_datetime(df['dia'], errors='coerce')
df = df[df['data'].notna()].copy()
print(f'Linhas de 2025+: {len(df)}')
print(f'Filiais: {df["restaurante"].unique()}')

conn = get_conn()
cur = conn.cursor()

ins = dup = err = 0
for _, row in df.iterrows():
    try:
        filial_key = str(row['restaurante']).strip()
        filial = MAPA_FILIAIS.get(filial_key, filial_key)
        data = row['data'].date()
        
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
            int(row['ANO']) if pd.notna(row.get('ANO')) else None,
            str(row['MÊS']) if pd.notna(row.get('MÊS')) else None,
            str(row['dia semana']) if pd.notna(row.get('dia semana')) else None,
            str(row['SEMANA']) if pd.notna(row.get('SEMANA')) else None,
            float(row['D.ROOM']) if pd.notna(row.get('D.ROOM')) else None,
            int(row["gc´s DR"]) if pd.notna(row.get("gc´s DR")) else None,
            float(row['DLV']) if pd.notna(row.get('DLV')) else None,
            int(row["TCs\nDLV"]) if pd.notna(row.get("TCs\nDLV")) else None,
            float(row['VENDA TOTAL']) if pd.notna(row.get('VENDA TOTAL')) else None,
            float(row['META VENDA R$']) if pd.notna(row.get('META VENDA R$')) else None,
            float(row['VENDA ANO-1']) if pd.notna(row.get('VENDA ANO-1')) else None,
            float(row['TICKET TOTAL']) if pd.notna(row.get('TICKET TOTAL')) else None,
            float(row['SALÃO (%)']) if pd.notna(row.get('SALÃO (%)')) else None,
            float(row['DLV (%)']) if pd.notna(row.get('DLV (%)')) else None,
            float(row['TOGO (%)']) if pd.notna(row.get('TOGO (%)')) else None,
            int(row['HDC ATUAL']) if pd.notna(row.get('HDC ATUAL')) else None,
            float(row['VENDA POR HDC']) if pd.notna(row.get('VENDA POR HDC')) else None,
        ))
        if cur.rowcount > 0:
            ins += 1
        else:
            dup += 1
    except Exception as e:
        conn.rollback()
        err += 1
        if err <= 3:
            print(f'  Erro: {e}')

conn.commit()
cur.execute('SELECT COUNT(id) FROM vendas_diarias')
print(f'\nInseridos: {ins} | Duplicatas: {dup} | Erros: {err}')
print(f'Total no banco: {cur.fetchone()[0]}')
cur.close()
conn.close()
print('Concluido!')
