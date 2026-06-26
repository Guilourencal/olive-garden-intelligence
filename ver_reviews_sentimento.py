import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql("SELECT filial, plataforma, sentimento, COUNT(*) as n FROM reviews GROUP BY filial, plataforma, sentimento ORDER BY filial, plataforma", conn)
conn.close()
df['filial'] = df['filial'].str.replace('Olive Garden - ','')
print(df.to_string(index=False))
