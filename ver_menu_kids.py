import psycopg2
from db import get_conn

conn = get_conn()
cur = conn.cursor()
cur.execute("""
    SELECT item, type, number_of_checks, gross_sales, ct_gross_total_check_avg, check_uplift
    FROM menu_analysis
    WHERE UPPER(item) LIKE '%KIDS%'
    ORDER BY semana_ref DESC, number_of_checks DESC
""")
rows = cur.fetchall()
cur.close()
conn.close()

print('=== MENU KIDS ===')
for row in rows:
    item, tipo, checks, gross, ct_avg, uplift = row
    print(f'Item: {item}')
    print(f'  Tipo: {tipo}')
    print(f'  Checks: {int(checks):,}'.replace(',','.'))
    print(f'  Gross Sales: R$ {gross:,.0f}'.replace(',','.'))
    print(f'  Check Completo Medio: R$ {ct_avg:.0f}' if ct_avg else '  Check Completo Medio: —')
    print(f'  Check Uplift: R$ {uplift:.0f}' if uplift else '  Check Uplift: —')
    print()
