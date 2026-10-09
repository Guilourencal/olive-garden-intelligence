from db import get_conn
import pandas as pd
import numpy as np
from datetime import date, timedelta
import calendar

conn = get_conn()
hoje = date.today()
ano, mes = hoje.year, hoje.month
dias_mes = calendar.monthrange(ano, mes)[1]
dias_realizados = hoje.day - 1  # ate ontem

df_real = pd.read_sql(f"""
    SELECT filial, SUM(venda_salao) as realizado, COUNT(*) as dias
    FROM vendas_diarias
    WHERE EXTRACT(month FROM data)={mes} AND EXTRACT(year FROM data)={ano}
    AND venda_salao > 0
    GROUP BY filial
""", conn)

df_hist = pd.read_sql(f"""
    SELECT filial, data, venda_salao,
           EXTRACT(dow FROM data) as dow
    FROM vendas_diarias
    WHERE EXTRACT(month FROM data)={mes}
    AND EXTRACT(year FROM data)={ano-1}
    AND venda_salao > 0
    ORDER BY filial, data
""", conn)
conn.close()

df_real["filial_curta"] = df_real["filial"].str.replace("Olive Garden - ","")
df_hist["filial_curta"] = df_hist["filial"].str.replace("Olive Garden - ","")

dias_restantes = dias_mes - dias_realizados
total_salao = 0

print(f"=== PROJECAO OUTUBRO {ano} ===")
print(f"Referencia: {hoje} | Dias realizados: {dias_realizados}/{dias_mes}")
print()
print(f"{'Filial':<20} {'Dias':>5} {'Realizado MTD':>16} {'Proj Resto':>14} {'Proj Mes':>13}")
print("-"*72)

for _, row in df_real.sort_values("realizado", ascending=False).iterrows():
    filial = row["filial"]
    realizado = row["realizado"]
    dias_real = row["dias"]
    media_dia = realizado / dias_real if dias_real > 0 else 0

    # Fator sazonalidade por dow usando historico ano anterior
    hist_fil = df_hist[df_hist["filial"]==filial]
    if len(hist_fil) > 0:
        media_hist = hist_fil["venda_salao"].mean()
        dow_factor = hist_fil.groupby("dow")["venda_salao"].mean() / media_hist if media_hist > 0 else {}
    else:
        dow_factor = {}

    # Projeta dias restantes
    proj_resto = 0
    for i in range(1, dias_restantes+1):
        dt = date(ano, mes, dias_realizados+i)
        dow = dt.weekday()
        fator = dow_factor.get(float((dow+1)%7), 1.0) if len(dow_factor) > 0 else 1.0
        proj_resto += media_dia * fator

    proj_mes = realizado + proj_resto
    total_salao += proj_mes
    nome = filial.replace("Olive Garden - ","")
    print(f"  {nome:<18} {int(dias_real):>5} R$ {realizado:>12,.0f} R$ {proj_resto:>11,.0f} R$ {proj_mes:>10,.0f}".replace(",","."))

print("-"*72)
print(f"  {'SALAO TOTAL':<18} {'':>5} {'':>16} {'':>14} R$ {total_salao:>10,.0f}".replace(",","."))
print()
print(f"  Dias restantes: {dias_restantes}")
