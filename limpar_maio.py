import psycopg2
from db import get_conn
conn = get_conn()
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
