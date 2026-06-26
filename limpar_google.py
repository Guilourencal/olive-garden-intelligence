import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()

cur.execute("""
    DELETE FROM reviews
    WHERE plataforma = 'Google Reviews'
    AND texto ~* '[a-zA-Z]{5,}'
    AND texto !~ '[à-úÀ-Ú]'
""")
print(f"Removidos: {cur.rowcount} reviews em inglês")
conn.commit()

cur.execute("SELECT COUNT(*) FROM reviews")
print(f"Total restante: {cur.fetchone()[0]}")

cur.close()
conn.close()