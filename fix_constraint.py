import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()
cur.execute("ALTER TABLE reviews DROP CONSTRAINT IF EXISTS reviews_autor_texto_filial_key")
conn.commit()
print('Constraint removida!')
cur.close()
conn.close()
