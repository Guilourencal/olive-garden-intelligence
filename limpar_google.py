import psycopg2

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
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