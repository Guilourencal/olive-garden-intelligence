import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'vendas' 
    ORDER BY ordinal_position
""")
for row in cur.fetchall():
    print(row)
cur.execute("SELECT * FROM vendas LIMIT 3")
print('\n--- Amostra ---')
cols = [d[0] for d in cur.description]
print(cols)
for row in cur.fetchall():
    print(row)
conn.close()
