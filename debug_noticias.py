import psycopg2
import pandas as pd
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
df = pd.read_sql("SELECT * FROM noticias ORDER BY publicado_em DESC", conn)
conn.close()

print(f'Total no banco: {len(df)}')
print(f'Tipo publicado_em: {df["publicado_em"].dtype}')
print(f'Valores publicado_em:')
print(df["publicado_em"].head())

data_corte = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
print(f'\nData corte: {data_corte}')

df_f = df[pd.to_datetime(df["publicado_em"], errors="coerce", utc=True) >= pd.Timestamp(data_corte, tz="UTC")]
print(f'Apos filtro: {len(df_f)}')
