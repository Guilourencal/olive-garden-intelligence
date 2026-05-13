import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
df = pd.read_sql("SELECT periodo, filial, logistica, pedidos, faturamento, ticket_medio, novos_clientes FROM ifood_vendas ORDER BY periodo, filial", conn)
conn.close()
print(df.to_string())
print(f"\nTipos:\n{df.dtypes}")
