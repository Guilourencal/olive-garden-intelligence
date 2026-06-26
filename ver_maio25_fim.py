import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
cur = conn.cursor()
cur.execute("""
    SELECT data, filial, venda_salao 
    FROM vendas_diarias 
    WHERE data IN ('2025-05-29','2025-05-30','2025-05-31')
    ORDER BY data, filial
""")
rows = cur.fetchall()
cur.close()
conn.close()

print('=== VENDAS 29-31/05/2025 ===')
total_dia = {}
for data, filial, venda in rows:
    filial_c = filial.replace('Olive Garden - ','')
    print(f'  {data} | {filial_c}: R$ {venda:,.0f}'.replace(',','.'))
    total_dia[str(data)] = total_dia.get(str(data), 0) + venda

print()
print('=== TOTAL REDE POR DIA ===')
for dia, total in sorted(total_dia.items()):
    print(f'  {dia}: R$ {total:,.0f}'.replace(',','.'))
