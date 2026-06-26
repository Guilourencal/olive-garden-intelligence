import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()

print('=== IFOOD REAL POR PERIODO ===')
cur.execute("""
    SELECT filial, periodo, SUM(faturamento) as fat, SUM(pedidos) as ped
    FROM ifood_vendas
    WHERE logistica = 'Entrega parceira'
    GROUP BY filial, periodo
    ORDER BY filial, periodo
""")
for r in cur.fetchall():
    print(f'  {r[0]} | {r[1]} | R$ {r[2]:,.0f} | {r[3]} ped'.replace(',','.'))

print()
print('=== VENDAS SALAO 2026 POR MES ===')
cur.execute("""
    SELECT filial,
           EXTRACT(month FROM data::date) as mes,
           SUM(venda_salao) as salao,
           SUM(meta_venda) as budget,
           SUM(gc_salao) as gcs
    FROM vendas_diarias
    WHERE EXTRACT(year FROM data::date) = 2026
    GROUP BY filial, EXTRACT(month FROM data::date)
    ORDER BY filial, mes
""")
for r in cur.fetchall():
    print(f'  {r[0]} | mes {int(r[1])} | salao R$ {r[2]:,.0f} | budget R$ {r[3]:,.0f} | GCs {int(r[4])}'.replace(',','.'))

cur.close()
conn.close()
