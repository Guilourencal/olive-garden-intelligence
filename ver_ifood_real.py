import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()

# Verificar faturamento real por filial em 2026
cur.execute("""
    SELECT filial, logistica, SUM(faturamento) as fat, COUNT(*) as n
    FROM ifood_vendas
    WHERE periodo LIKE '%2026%'
    GROUP BY filial, logistica
    ORDER BY filial, logistica
""")
print('=== IFOOD_VENDAS 2026 ===')
for r in cur.fetchall():
    print(f'  {r[0]} | {r[1]} | R$ {r[2]:,.0f} | {r[3]} registros'.replace(',','.'))

cur.execute("""
    SELECT filial, SUM(venda_salao) as salao
    FROM vendas_diarias
    WHERE EXTRACT(year FROM data) = 2026
    AND filial IN ('Olive Garden - Morumbi','Olive Garden - Aricanduva')
    GROUP BY filial
""")
print()
print('=== VENDAS_DIARIAS 2026 ===')
for r in cur.fetchall():
    print(f'  {r[0]} | R$ {r[1]:,.0f}'.replace(',','.'))

cur.close()
conn.close()
