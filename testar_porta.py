import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=5432,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
print('Conectado!')
conn.close()
