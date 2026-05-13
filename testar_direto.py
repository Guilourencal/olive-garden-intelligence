import psycopg2
conn = psycopg2.connect(
    host='db.rvauallshhozpruvusrr.supabase.co',
    port=5432,
    user='postgres',
    password='olivegarden2233@',
    database='postgres'
)
print('Conectado!')
conn.close()
