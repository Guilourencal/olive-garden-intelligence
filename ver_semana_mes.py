import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql('SELECT data, venda_salao FROM vendas_diarias ORDER BY data', conn)
conn.close()

df['data'] = pd.to_datetime(df['data'])
df['dia_mes'] = df['data'].dt.day
df['semana_mes'] = pd.cut(df['dia_mes'], bins=[0,7,14,21,31], labels=['S1','S2','S3','S4'])

print('=== VENDA MEDIA POR SEMANA DO MES (rede completa) ===')
resumo = df.groupby('semana_mes')['venda_salao'].agg(['mean','count']).round(0)
resumo.columns = ['media_diaria','n_obs']
print(resumo.to_string())

print()
print('=== INDICE vs S1 ===')
base = resumo.loc['S1','media_diaria']
for s in ['S1','S2','S3','S4']:
    idx = resumo.loc[s,'media_diaria'] / base * 100
    print(f'  {s}: {idx:.1f}%')
