from db import get_conn
import pandas as pd
from datetime import date
conn = get_conn()
hoje = date.today()
df = pd.read_sql(f"""
    SELECT filial, SUM(venda_salao) as salao, SUM(gc_salao) as gc,
           COUNT(*) as dias, ROUND(AVG(venda_salao)::numeric,0) as media_dia
    FROM vendas_diarias
    WHERE EXTRACT(month FROM data)={hoje.month}
    AND EXTRACT(year FROM data)={hoje.year}
    AND venda_salao > 0
    GROUP BY filial ORDER BY salao DESC
""", conn)
conn.close()
df["filial_curta"] = df["filial"].str.replace("Olive Garden - ","")
total = df["salao"].sum()
print(f"=== Ranking MTD Outubro {hoje.year} ===")
print(df[["filial_curta","salao","gc","dias","media_dia"]].to_string(index=False))
print(f"\nTotal rede salao: R$ {total:,.0f}".replace(",","."))
