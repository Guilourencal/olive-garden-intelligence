import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql("SELECT periodo, filial, logistica, pedidos, faturamento, ticket_medio, novos_clientes FROM ifood_vendas ORDER BY periodo, filial", conn)
conn.close()
print(df.to_string())
print(f"\nTipos:\n{df.dtypes}")
