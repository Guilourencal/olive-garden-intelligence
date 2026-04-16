import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)

df = pd.read_sql("SELECT texto FROM reviews WHERE plataforma = 'Google Reviews' LIMIT 5", conn)
print(df["texto"].to_string())
conn.close()