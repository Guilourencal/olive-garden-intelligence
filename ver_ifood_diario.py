import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
cur = conn.cursor()

# Ver se ja temos periodos de 1 dia no banco
cur.execute("""
    SELECT periodo, SUM(faturamento) as fat, SUM(pedidos) as ped
    FROM ifood_vendas
    WHERE logistica = 'Entrega parceira'
    AND SUBSTRING(periodo, 1, 10) = SUBSTRING(periodo, 14, 10)
    GROUP BY periodo
    ORDER BY periodo DESC
    LIMIT 10
""")
rows = cur.fetchall()
print('Periodos de 1 dia no banco:')
for r in rows:
    print(f'  {r[0]} | R$ {r[1]:,.0f} | {r[2]} ped'.replace(',','.'))

cur.close()
conn.close()
