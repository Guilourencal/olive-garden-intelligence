import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT DISTINCT periodo, arquivo_origem FROM ifood_vendas ORDER BY periodo DESC LIMIT 10")
for row in cur.fetchall():
    print(row)
cur.close()
conn.close()
