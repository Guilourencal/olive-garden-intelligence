import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT DISTINCT periodo FROM ifood_vendas ORDER BY periodo DESC LIMIT 10")
for row in cur.fetchall():
    print(row[0])
cur.close()
conn.close()
