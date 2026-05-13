novo = '''import pandas as pd
import psycopg2
from datetime import datetime

# Google — CSV
google = pd.read_csv("reviews_google_bruto.csv", encoding="utf-8-sig")
print(f"Google: {len(google)} reviews")
print(f"  Primeiro: {google['texto'].iloc[0][:60]}")

# TripAdvisor — CSV
tripadvisor = pd.read_csv("reviews_tripadvisor_bruto.csv", encoding="utf-8-sig")
print(f"TripAdvisor: {len(tripadvisor)} reviews")

# iFood — lendo direto do Supabase (relatorio oficial)
conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
cur = conn.cursor()
cur.execute("SELECT filial, plataforma, nota, texto, data_coleta FROM reviews WHERE plataforma = 'iFood' AND fonte_id IS NOT NULL ORDER BY data_coleta DESC")
rows = cur.fetchall()
cur.close()
conn.close()

if rows:
    ifood = pd.DataFrame(rows, columns=["filial","plataforma","nota","texto","data_coleta"])
    ifood["autor"] = ""
    ifood["data_original"] = ifood["data_coleta"]
else:
    ifood = pd.DataFrame(columns=["filial","plataforma","nota","texto","data_coleta","autor","data_original"])
print(f"iFood: {len(ifood)} reviews")

# Unifica
df = pd.concat([google, tripadvisor, ifood], ignore_index=True)

# Normaliza filiais
nomes_map = {
    "Olive Garden - GRU2": "Olive Garden - Guarulhos GRU2",
    "Olive Garden - GRU3": "Olive Garden - Guarulhos GRU3",
    "Olive Garden - Campinas": "Olive Garden - Dom Pedro",
}
df["filial"] = df["filial"].replace(nomes_map)
df.to_csv("reviews_unificado.csv", index=False, encoding="utf-8-sig")
print(f"\\nTotal unificado: {len(df)}")
print(f"\\nPor plataforma:")
print(df["plataforma"].value_counts().to_string())
print(f"\\nFiliais:")
print(df["filial"].value_counts().to_string())
'''
open('unificar_dados.py', 'w', encoding='utf-8').write(novo)
print('Feito!')
