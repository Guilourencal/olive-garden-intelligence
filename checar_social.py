import psycopg2
import pandas as pd
from datetime import datetime

conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()

cur.execute('DELETE FROM social')
print(f'Registros removidos: {cur.rowcount}')
conn.commit()

df = pd.read_csv('social_instagram_bruto.csv', encoding='utf-8-sig')
df['data_original'] = pd.to_datetime(df['data_original'], errors='coerce', utc=True)
data_corte = pd.Timestamp('2026-03-01', tz='UTC')
df_filtrado = df[df['data_original'] >= data_corte].copy()
df_todos = df.copy()

print(f'Total coletado: {len(df)}')
print(f'A partir de 01/03/2026: {len(df_filtrado)}')
print(f'Periodo mais antigo: {df["data_original"].min()}')
print(f'Periodo mais recente: {df["data_original"].max()}')

cur.close()
conn.close()
