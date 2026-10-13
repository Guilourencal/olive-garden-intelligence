import os, sys, re
import pandas as pd
from datetime import datetime
from db import get_conn

# Pasta dos arquivos Keeta
MES_PT = {1:"Janeiro",2:"Fevereiro",3:"Marco",4:"Abril",5:"Maio",6:"Junho",
          7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}
mes_atual = MES_PT[datetime.now().month]
PASTA = os.path.join("data", "keeta", mes_atual)

# Mapeamento nome arquivo -> filial
FILIAL_MAP = {
    "morumbi":      "Olive Garden - Morumbi",
    "centernorte":  "Olive Garden - Center Norte",
    "center_norte": "Olive Garden - Center Norte",
    "dompedro":     "Olive Garden - Dom Pedro",
    "dom_pedro":    "Olive Garden - Dom Pedro",
    "aricanduva":   "Olive Garden - Aricanduva",
    "tambore":      "Olive Garden - Tambore",
    "gru2":         "Olive Garden - Guarulhos GRU2",
    "gru3":         "Olive Garden - Guarulhos GRU3",
}

def detectar_filial(nome_arquivo):
    n = nome_arquivo.lower().replace(" ", "_")
    for chave, filial in FILIAL_MAP.items():
        if chave in n:
            return filial
    return None

if not os.path.exists(PASTA):
    os.makedirs(PASTA, exist_ok=True)
    print(f"Pasta criada: {PASTA}")

arquivos = [f for f in os.listdir(PASTA) if f.endswith(".xlsx")]
if not arquivos:
    print(f"Nenhum arquivo .xlsx em {PASTA}")
    sys.exit(0)

conn = get_conn()
cur = conn.cursor()
total_insert = total_skip = total_erro = 0

for arq in sorted(arquivos):
    filial = detectar_filial(arq)
    if not filial:
        print(f"  AVISO: nao identificou filial em '{arq}' ? renomeie com nome da unidade")
        total_erro += 1
        continue

    path = os.path.join(PASTA, arq)
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = ["data","ganhos_liquidos","vendas_itens","outros_ganhos",
                  "despesa","comissao","outras_despesas"]
    df = df[pd.to_numeric(df["data"], errors="coerce").notna()]
    df["data"] = pd.to_datetime(df["data"].astype(str), format="%Y%m%d").dt.date
    df = df[df["vendas_itens"] > 0]

    insert = skip = 0
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO keeta_diario
                (data, filial, ganhos_liquidos, vendas_itens, outros_ganhos,
                 despesa, comissao, outras_despesas, arquivo_origem)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (data, filial) DO UPDATE SET
                ganhos_liquidos=EXCLUDED.ganhos_liquidos,
                vendas_itens=EXCLUDED.vendas_itens,
                outros_ganhos=EXCLUDED.outros_ganhos,
                despesa=EXCLUDED.despesa,
                comissao=EXCLUDED.comissao,
                outras_despesas=EXCLUDED.outras_despesas,
                arquivo_origem=EXCLUDED.arquivo_origem
        """, (row["data"], filial,
              float(row["ganhos_liquidos"]), float(row["vendas_itens"]),
              float(row["outros_ganhos"]), float(row["despesa"]),
              float(row["comissao"]), float(row["outras_despesas"]), arq))
        if cur.rowcount == 1:
            insert += 1
        else:
            skip += 1

    conn.commit()
    print(f"  {filial.replace('Olive Garden - ','')} | {arq} | {insert} inseridos, {skip} atualizados")
    total_insert += insert
    total_skip += skip

print(f"\nTotal: {total_insert} inseridos | {total_skip} atualizados | {total_erro} erros")

# Resumo banco
cur.execute("""
    SELECT filial, COUNT(*) as dias, SUM(vendas_itens) as gmv,
           SUM(ganhos_liquidos) as liquido, MIN(data) as ini, MAX(data) as fim
    FROM keeta_diario
    GROUP BY filial ORDER BY gmv DESC
""")
rows = cur.fetchall()
if rows:
    print("\n=== KEETA NO BANCO ===")
    for r in rows:
        nome = r[0].replace("Olive Garden - ","")
        print(f"  {nome} | {r[1]} dias | GMV R${float(r[2]):,.0f} | Liq R${float(r[3]):,.0f} | {r[4]} a {r[5]}".replace(",","."))
conn.close()
