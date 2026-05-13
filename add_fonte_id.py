import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()
cur.execute("ALTER TABLE reviews ADD COLUMN IF NOT EXISTS fonte_id VARCHAR(255)")
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS reviews_fonte_id_idx ON reviews(fonte_id) WHERE fonte_id IS NOT NULL")
conn.commit()
print('Coluna fonte_id adicionada!')
cur.close()
conn.close()
