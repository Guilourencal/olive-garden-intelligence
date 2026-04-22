import psycopg2

conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()

print('=== REVIEWS ===')
cur.execute('SELECT plataforma, COUNT(id), MAX(data_coleta) FROM reviews GROUP BY plataforma ORDER BY plataforma')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]} reviews | ultima coleta: {row[2]}')

print()
print('=== SOCIAL ===')
cur.execute('SELECT COUNT(id), MAX(data_coleta) FROM social')
row = cur.fetchone()
print(f'  Total: {row[0]} comentarios | ultima coleta: {row[1]}')

print()
print('=== GMB por filial ===')
cur.execute('SELECT filial, COUNT(id), MAX(data_coleta), ROUND(AVG(nota)::numeric,2) FROM reviews WHERE plataforma=\'Google Reviews\' GROUP BY filial ORDER BY filial')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]} reviews | nota: {row[3]} | coleta: {row[2]}')

cur.close()
conn.close()
