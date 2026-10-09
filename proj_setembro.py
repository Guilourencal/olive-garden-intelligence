from db import get_conn
import pandas as pd
import numpy as np
import calendar
from datetime import date

conn = get_conn()
hoje = date.today()
mes_proj = hoje.month
ano_proj = hoje.year
dias_no_mes = calendar.monthrange(ano_proj, mes_proj)[1]

df_vd = pd.read_sql("SELECT data, filial, venda_salao FROM vendas_diarias WHERE venda_salao > 0 ORDER BY data", conn)
df_vd["data"] = pd.to_datetime(df_vd["data"])
df_vd["filial_curta"] = df_vd["filial"].str.replace("Olive Garden - ","",regex=False)
df_vd["dow"] = df_vd["data"].dt.dayofweek
df_vd["mes_n"] = df_vd["data"].dt.month

filiais = ["Morumbi","Center Norte","Dom Pedro","Aricanduva","Guarulhos GRU2","Guarulhos GRU3","Tambore"]
df_mes = df_vd[(df_vd["data"].dt.month==mes_proj)&(df_vd["data"].dt.year==ano_proj)]
dias_real = int(df_mes["data"].dt.day.max()) if len(df_mes) > 0 else 0

print(f"=== PROJECAO SETEMBRO {ano_proj} ===")
print(f"Referencia: {hoje} | Dias realizados: {dias_real}/{dias_no_mes}")
print()

resultados = []
total_real = 0
total_proj = 0

for fil in filiais:
    dff = df_vd[df_vd["filial_curta"]==fil].copy()
    real_mes = dff[(dff["data"].dt.month==mes_proj)&(dff["data"].dt.year==ano_proj)]["venda_salao"].sum()
    dias_fil = len(dff[(dff["data"].dt.month==mes_proj)&(dff["data"].dt.year==ano_proj)])
    if len(dff) >= 10:
        media = dff["venda_salao"].mean()
        fdow = dff.groupby("dow")["venda_salao"].mean() / media
        fmes = dff.groupby("mes_n")["venda_salao"].mean() / media
        df_rec = dff[(dff["data"].dt.month==mes_proj)&(dff["data"].dt.year==ano_proj)]
        frec = df_rec["venda_salao"].mean() / media if len(df_rec) >= 5 else 1.0
        frec = float(np.clip(frec, 0.80, 1.30))
        proj_rest = sum(
            media * float(fdow.get(pd.Timestamp(ano_proj, mes_proj, d).dayofweek, 1.0)) *
            float(fmes.get(mes_proj, 1.0)) * frec
            for d in range(dias_real+1, dias_no_mes+1)
        )
        proj_total = real_mes + proj_rest
    else:
        proj_total = real_mes
        proj_rest = 0
    resultados.append({"filial": fil, "real": real_mes, "dias": dias_fil, "proj_rest": proj_rest, "proj_total": proj_total})
    total_real += real_mes
    total_proj += proj_total

# iFood setembro - mes corrente
cur = conn.cursor()
mes_str = f"{mes_proj:02d}/{ano_proj}"
cur.execute(f"SELECT SUM(faturamento), SUM(pedidos) FROM ifood_vendas WHERE periodo LIKE '%{mes_str}%' AND logistica='Entrega parceira'")
r = cur.fetchone()
if_mtd = float(r[0] or 0)
proj_if_rest = if_mtd / dias_real * (dias_no_mes - dias_real) if dias_real > 0 else 0
if_total = if_mtd + proj_if_rest

print(f"{'Filial':<20} {'Dias':>5} {'Realizado MTD':>14} {'Proj Resto':>14} {'Proj Mes':>14}")
print("-"*72)
for r in sorted(resultados, key=lambda x: -x["proj_total"]):
    print(f"  {r['filial']:<18} {r['dias']:>5} R${r['real']:>12,.0f} R${r['proj_rest']:>12,.0f} R${r['proj_total']:>12,.0f}".replace(",","."))
print("-"*72)
print(f"  {'SALAO TOTAL':<18} {'':>5} R${total_real:>12,.0f} R${total_proj-total_real:>12,.0f} R${total_proj:>12,.0f}".replace(",","."))
print(f"  {'iFOOD SET':<18} {'':>5} R${if_mtd:>12,.0f} R${proj_if_rest:>12,.0f} R${if_total:>12,.0f}".replace(",","."))
print("-"*72)
print(f"  {'REDE TOTAL':<18} {'':>5} {'':>14} {'':>14} R${total_proj+if_total:>12,.0f}".replace(",","."))
conn.close()
