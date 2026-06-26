import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()

# Dados reais iFood
df_if = pd.read_sql("""
    SELECT filial, periodo, SUM(faturamento) as fat, SUM(pedidos) as ped
    FROM ifood_vendas
    WHERE logistica = 'Entrega parceira'
    GROUP BY filial, periodo
    ORDER BY filial, periodo
""", conn)

# Dados reais vendas
df_vd = pd.read_sql("""
    SELECT filial, 
           EXTRACT(month FROM data) as mes,
           EXTRACT(year FROM data) as ano,
           SUM(venda_salao) as salao,
           SUM(meta_venda) as budget,
           SUM(gc_salao) as gcs
    FROM vendas_diarias
    WHERE EXTRACT(year FROM data) = 2026
    GROUP BY filial, mes, ano
    ORDER BY filial, mes
""", conn)
conn.close()

print('=== IFOOD REAL ===')
print(df_if.to_string(index=False))
print()
print('=== VENDAS REAIS 2026 ===')
print(df_vd.to_string(index=False))
