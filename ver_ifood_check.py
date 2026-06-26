import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
cur = conn.cursor()

print('=== IFOOD_VENDAS — TODOS OS PERIODOS ===')
cur.execute("SELECT periodo, logistica, SUM(faturamento) as fat, SUM(pedidos) as ped FROM ifood_vendas GROUP BY periodo, logistica ORDER BY periodo DESC")
for r in cur.fetchall():
    print(f'  {r[0]} | {r[1]} | Fat: R$ {r[2]:,.0f} | Ped: {r[3]}'.replace(',','.'))

print()
print('=== JUNHO 2026 — DETALHE ===')
cur.execute("SELECT periodo, filial, logistica, faturamento, pedidos FROM ifood_vendas WHERE periodo LIKE '%06/2026%' ORDER BY filial")
for r in cur.fetchall():
    print(f'  {r[0]} | {r[1]} | {r[2]} | R$ {r[3]:,.0f} | {r[4]} ped'.replace(',','.'))

cur.close()
conn.close()
