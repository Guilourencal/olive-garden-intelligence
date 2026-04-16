import psycopg2

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
cur = conn.cursor()
cur.execute("SELECT DISTINCT filial FROM reviews ORDER BY filial")
for row in cur.fetchall():
    print(row[0])
conn.close()