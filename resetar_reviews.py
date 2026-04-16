import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
cur = conn.cursor()

# Apaga tudo
cur.execute("DELETE FROM reviews")
print(f"Reviews removidos: {cur.rowcount}")
conn.commit()

# Lê o CSV classificado
df = pd.read_csv("reviews_classificado.csv", encoding="utf-8-sig")
df = df.where(pd.notnull(df), None)

# Normaliza filiais
nomes_map = {
    "Olive Garden - GRU2": "Olive Garden - Guarulhos GRU2",
    "Olive Garden - GRU3": "Olive Garden - Guarulhos GRU3",
    "Olive Garden - Campinas": "Olive Garden - Dom Pedro",
}
df["filial"] = df["filial"].replace(nomes_map)

inseridos = 0
for _, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO reviews (filial, plataforma, autor, nota, texto,
                data_original, data_coleta, nota_geral_filial,
                total_avaliacoes_filial, sentimento, sentimento_score, tema)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row.get("filial"), row.get("plataforma"), row.get("autor"),
            row.get("nota"), row.get("texto"), row.get("data_original"),
            row.get("data_coleta"), row.get("nota_geral_filial"),
            row.get("total_avaliacoes_filial"), row.get("sentimento"),
            row.get("sentimento_score"), row.get("tema")
        ))
        inseridos += 1
    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")

conn.commit()
cur.execute("SELECT COUNT(*) FROM reviews")
print(f"Total no Supabase: {cur.fetchone()[0]}")
cur.execute("SELECT DISTINCT filial FROM reviews ORDER BY filial")
print("\nFiliais:")
for row in cur.fetchall():
    print(f"  {row[0]}")
cur.close()
conn.close()
print("\nConcluído!")