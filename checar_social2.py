import psycopg2
from db import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute('SELECT COUNT(id), MAX(data_coleta) FROM social')
row = cur.fetchone()
print(f'Total: {row[0]} | Ultima coleta: {row[1]}')
cur.execute('SELECT sentimento, COUNT(id) FROM social GROUP BY sentimento')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]}')
cur.close()
conn.close()
