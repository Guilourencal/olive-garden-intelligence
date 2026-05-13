import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()

periodo_antigo = '01/05/2026 - 05/05/2026'

cur.execute('DELETE FROM ifood_vendas WHERE periodo = %s', (periodo_antigo,))
print(f'ifood_vendas: {cur.rowcount} removidos')
cur.execute('DELETE FROM ifood_horarios WHERE periodo = %s', (periodo_antigo,))
print(f'ifood_horarios: {cur.rowcount} removidos')
cur.execute('DELETE FROM ifood_pagamentos WHERE periodo = %s', (periodo_antigo,))
print(f'ifood_pagamentos: {cur.rowcount} removidos')
cur.execute('DELETE FROM ifood_dias WHERE periodo = %s', (periodo_antigo,))
print(f'ifood_dias: {cur.rowcount} removidos')

conn.commit()

cur.execute('SELECT DISTINCT periodo FROM ifood_vendas ORDER BY periodo')
print('\nPeriodos restantes:')
for row in cur.fetchall():
    print(f'  {row[0]}')

cur.close()
conn.close()
print('\nFeito!')
