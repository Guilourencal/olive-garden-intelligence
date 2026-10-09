from db import get_conn
import pandas as pd
conn = get_conn()
df = pd.read_sql("""
    SELECT filial, SUM(venda_salao) as salao, SUM(gc_salao) as gc,
           COUNT(*) as dias, ROUND(AVG(venda_salao)::numeric,0) as media_dia
    FROM vendas_diarias
    WHERE EXTRACT(month FROM data)=9 AND EXTRACT(year FROM data)=2026
    GROUP BY filial ORDER BY salao DESC
""", conn)
print("=== Ranking MTD Setembro ===")
print(df.to_string(index=False))
print(f"\nTotal rede salao: R$ {df['salao'].sum():,.0f}".replace(",","."))
conn.close()
