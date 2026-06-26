import psycopg2
from db import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute('SELECT filial, COUNT(id), MIN(data), MAX(data), SUM(venda_total) FROM vendas_diarias GROUP BY filial ORDER BY filial')
for row in cur.fetchall():
    print(f'{row[0]}: {row[1]} dias | {row[2]} a {row[3]} | R$ {row[4]:,.0f}')
cur.close()
conn.close()
