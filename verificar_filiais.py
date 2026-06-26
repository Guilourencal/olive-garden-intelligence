import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT DISTINCT filial FROM reviews ORDER BY filial")
for row in cur.fetchall():
    print(row[0])
conn.close()