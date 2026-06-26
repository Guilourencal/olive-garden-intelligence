import psycopg2
from db import get_conn
cur = get_conn().cursor()
cur.execute("SELECT DISTINCT periodo FROM ifood_vendas ORDER BY periodo DESC LIMIT 5")
for r in cur.fetchall(): print(r[0])
