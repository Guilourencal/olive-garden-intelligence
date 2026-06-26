import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT filial, venda_salao FROM vendas_diarias WHERE data='2026-05-26' ORDER BY filial")
rows = cur.fetchall()
cur.close()
conn.close()

print('=== FATURAMENTO 26/05/2026 ===')
total = 0
for filial, venda in rows:
    filial_c = filial.replace('Olive Garden - ', '')
    print(f'  {filial_c}: R$ {venda:,.0f}'.replace(',','.'))
    total += venda
print(f'  TOTAL REDE: R$ {total:,.0f}'.replace(',','.'))
