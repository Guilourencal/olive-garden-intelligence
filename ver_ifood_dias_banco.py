import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT DISTINCT periodo FROM ifood_dias ORDER BY periodo DESC LIMIT 5")
print('Periodos ifood_dias:')
for r in cur.fetchall(): print(' ', r[0])
cur.execute("SELECT dia_semana, SUM(pedidos) FROM ifood_dias WHERE periodo LIKE '%06/2026%' GROUP BY dia_semana")
print('Dias junho 2026:')
for r in cur.fetchall(): print(f'  {r[0]}: {r[1]} pedidos')
cur.close()
conn.close()
