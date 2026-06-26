import psycopg2
from db import get_conn
cur = get_conn().cursor()
cur.execute("SELECT plataforma, COUNT(*), AVG(nota) FROM reviews GROUP BY plataforma")
for r in cur.fetchall():
    print(f'{r[0]}: {r[1]} reviews | nota media {r[2]:.1f}' if r[2] else f'{r[0]}: {r[1]} reviews')
