import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()
cur.execute('SELECT filial, COUNT(id), MIN(data), MAX(data), SUM(venda_total) FROM vendas_diarias GROUP BY filial ORDER BY filial')
for row in cur.fetchall():
    print(f'{row[0]}: {row[1]} dias | {row[2]} a {row[3]} | R$ {row[4]:,.0f}')
cur.close()
conn.close()
