import psycopg2
from db import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute("DELETE FROM ifood_vendas WHERE arquivo_origem = 'iFood_Vendas_Maio2026_20.xlsx'")
cur.execute("DELETE FROM ifood_horarios WHERE arquivo_origem = 'iFood_Vendas_Maio2026_20.xlsx'")
cur.execute("DELETE FROM ifood_pagamentos WHERE arquivo_origem = 'iFood_Vendas_Maio2026_20.xlsx'")
cur.execute("DELETE FROM ifood_dias WHERE arquivo_origem = 'iFood_Vendas_Maio2026_20.xlsx'")
conn.commit()
print('Registros removidos. Reimportando...')
cur.close()
conn.close()
