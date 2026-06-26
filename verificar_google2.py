import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()

cur.execute("SELECT id, filial, texto FROM reviews WHERE plataforma = 'Google Reviews'")
rows = cur.fetchall()
for row in rows:
    print(f"ID: {row[0]} | Filial: {row[1]}")
    print(f"Texto: {row[2]}")
    print("---")

conn.close()