import psycopg2
conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()
periodo = '01/05/2026 - 10/05/2026'
cur.execute('DELETE FROM ifood_vendas WHERE periodo = %s', (periodo,))
cur.execute('DELETE FROM ifood_horarios WHERE periodo = %s', (periodo,))
cur.execute('DELETE FROM ifood_pagamentos WHERE periodo = %s', (periodo,))
cur.execute('DELETE FROM ifood_dias WHERE periodo = %s', (periodo,))
conn.commit()
print('Periodo de Maio removido!')
cur.close()
conn.close()
