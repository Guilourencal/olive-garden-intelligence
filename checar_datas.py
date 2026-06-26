import psycopg2
from db import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT plataforma, MAX(data_coleta), COUNT(id) FROM reviews GROUP BY plataforma ORDER BY plataforma")
for row in cur.fetchall():
    print(f'{row[0]}: {row[2]} reviews | ultima coleta: {row[1]}')
cur.close()
conn.close()
