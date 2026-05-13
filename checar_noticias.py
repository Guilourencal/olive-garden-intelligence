import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()
cur.execute('SELECT categoria, titulo, publicado_em FROM noticias ORDER BY publicado_em DESC')
for row in cur.fetchall():
    print(f'[{row[0]}] {row[1][:60]} | {row[2]}')
cur.close()
conn.close()
