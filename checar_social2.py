import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()
cur.execute('SELECT COUNT(id), MAX(data_coleta) FROM social')
row = cur.fetchone()
print(f'Total: {row[0]} | Ultima coleta: {row[1]}')
cur.execute('SELECT sentimento, COUNT(id) FROM social GROUP BY sentimento')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]}')
cur.close()
conn.close()
