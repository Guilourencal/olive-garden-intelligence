import psycopg2
from db import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT DISTINCT periodo, restaurant FROM pesquisa_performance ORDER BY periodo, restaurant")
for row in cur.fetchall():
    print(f'{row[0]} | {row[1]}')
cur.close()
conn.close()
