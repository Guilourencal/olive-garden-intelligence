import psycopg2
from db import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute('SELECT categoria, titulo, publicado_em FROM noticias ORDER BY publicado_em DESC')
for row in cur.fetchall():
    print(f'[{row[0]}] {row[1][:60]} | {row[2]}')
cur.close()
conn.close()
