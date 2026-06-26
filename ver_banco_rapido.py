import psycopg2
from db import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute('SELECT COUNT(*), MIN(data), MAX(data) FROM vendas_diarias')
print(cur.fetchone())
cur.close()
conn.close()
