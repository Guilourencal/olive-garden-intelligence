import psycopg2

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
cur = conn.cursor()

cur.execute("SELECT id, filial, texto FROM reviews WHERE plataforma = 'Google Reviews'")
rows = cur.fetchall()
for row in rows:
    print(f"ID: {row[0]} | Filial: {row[1]}")
    print(f"Texto: {row[2]}")
    print("---")

conn.close()