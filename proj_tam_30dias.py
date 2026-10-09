# proj_tam_30dias.py
# Projecao dinamica: sempre os ultimos 30 dias de Tambore no banco
from db import get_conn
import pandas as pd
import numpy as np
from datetime import timedelta

conn = get_conn()

df = pd.read_sql("""
    SELECT data, venda_salao, gc_salao, meta_venda
    FROM vendas_diarias
    WHERE filial LIKE '%Tambore%'
    ORDER BY data
""", conn)
conn.close()

df["data"] = pd.to_datetime(df["data"])
df = df.sort_values("data").reset_index(drop=True)

# Janela: ultimo dia disponivel - 29 dias ate ultimo dia
ultimo_dia = df["data"].max()
primeiro_dia = ultimo_dia - timedelta(days=29)
df_win = df[df["data"] >= primeiro_dia].reset_index(drop=True)

# Dados reais da janela
n_real = len(df_win)
media_base = df_win["venda_salao"].astype(float).mean()

# Fator por dia da semana (sobre todos os dados historicos de Tambore)
df["dow"] = df["data"].dt.dayofweek
media_geral = df["venda_salao"].astype(float).mean()
fdow = (df.groupby("dow")["venda_salao"].mean() / media_geral).to_dict()

# GC medio por dia da semana
fdow_gc = df.groupby("dow")["gc_salao"].mean().to_dict()

# Projeta dias que faltam para completar 30 dias a partir do primeiro da janela
dias_proj = []
for i in range(n_real, 30):
    dt = primeiro_dia + timedelta(days=i)
    dow = dt.dayofweek
    venda_proj = media_base * fdow.get(dow, 1.0)
    gc_proj = fdow_gc.get(dow, media_base / 130)
    dias_proj.append({"data": dt, "venda": venda_proj, "gc": int(gc_proj), "tipo": "PROJ"})

# Calcula ticket medio
total_venda_real = df_win["venda_salao"].astype(float).sum()
total_gc_real = df_win["gc_salao"].astype(float).sum()
ticket_medio = total_venda_real / total_gc_real if total_gc_real > 0 else 0

print(f"=== TAMBORE — ULTIMOS 30 DIAS ===")
print(f"Periodo: {primeiro_dia.strftime('%d/%m/%Y')} a {(primeiro_dia + timedelta(days=29)).strftime('%d/%m/%Y')}")
print(f"Base: media diaria R$ {media_base:,.0f} | {n_real} dias realizados".replace(",","."))
print()
print(f"{'Dia':<4} {'Data':<12} {'Dia Sem':<6} {'Venda':>10} {'GC':>5} {'Meta':>10} {'vs Meta':>8} {'Tipo'}")
print("-"*72)

total_venda = 0
total_gc = 0

for i in range(30):
    dt = primeiro_dia + timedelta(days=i)
    dia_num = i + 1
    dow_nome = ["Seg","Ter","Qua","Qui","Sex","Sab","Dom"][dt.dayofweek]

    if i < n_real:
        row = df_win.iloc[i]
        venda = float(row["venda_salao"])
        gc = int(row["gc_salao"])
        meta = float(row["meta_venda"])
        vs = (venda/meta-1)*100 if meta > 0 else 0
        vs_str = f"{vs:+.1f}%"
        tipo = "REAL"
    else:
        idx_proj = i - n_real
        venda = dias_proj[idx_proj]["venda"]
        gc = dias_proj[idx_proj]["gc"]
        meta = 0
        vs_str = "?"
        tipo = "PROJ"

    total_venda += venda
    total_gc += gc
    meta_str = f"R$ {meta:>9,.0f}".replace(",",".") if meta > 0 else f"{'?':>12}"
    print(f"  {dia_num:<3} {dt.strftime('%d/%m')} {dt.strftime('%a'):<4} {dow_nome:<4} R$ {venda:>9,.0f} {gc:>5} {meta_str} {vs_str:>8} {tipo}".replace(",","."))

print("-"*72)
proj_total = total_venda + sum(d["venda"] for d in dias_proj[max(0, 30-n_real):])
print(f"  {'TOTAL':<30} R$ {total_venda:>9,.0f} {total_gc:>5}".replace(",","."))
print()
print(f"  Media diaria real:      R$ {media_base:,.0f}".replace(",","."))
print(f"  Projecao 30 dias:       R$ {total_venda:,.0f}".replace(",","."))
print(f"  GC total:               {total_gc:,}".replace(",","."))
print(f"  Ticket medio:           R$ {ticket_medio:.2f}")
