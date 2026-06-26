import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql("SELECT filial, pedidos FROM ifood_vendas WHERE logistica='Entrega parceira' AND periodo LIKE '%05/2026%' ORDER BY filial", conn)
conn.close()
print(df.to_string(index=False))
print()
print('Total pedidos Mai:', int(df['pedidos'].sum()))
