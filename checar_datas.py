import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()
cur.execute("SELECT plataforma, MAX(data_coleta), COUNT(id) FROM reviews GROUP BY plataforma ORDER BY plataforma")
for row in cur.fetchall():
    print(f'{row[0]}: {row[2]} reviews | ultima coleta: {row[1]}')
cur.close()
conn.close()
