import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql("SELECT DISTINCT filial, periodo FROM ifood_vendas WHERE logistica='Entrega parceira' ORDER BY periodo", conn)
conn.close()
print(df.to_string(index=False))
