import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)

df = pd.read_sql("SELECT id, plataforma, nota, sentimento, sentimento_score, texto FROM reviews ORDER BY sentimento_score ASC", conn)
conn.close()

# Casos suspeitos: nota alta mas sentimento negativo
suspeitos_1 = df[(df["nota"] >= 4) & (df["sentimento"] == "Negativo")]
print(f"Nota >= 4 mas Negativo: {len(suspeitos_1)}")
print(suspeitos_1[["id", "plataforma", "nota", "sentimento", "sentimento_score", "texto"]].head(10).to_string())

print("\n" + "="*60 + "\n")

# Casos suspeitos: nota baixa mas sentimento positivo
suspeitos_2 = df[(df["nota"] <= 2) & (df["sentimento"] == "Positivo")]
print(f"Nota <= 2 mas Positivo: {len(suspeitos_2)}")
print(suspeitos_2[["id", "plataforma", "nota", "sentimento", "sentimento_score", "texto"]].head(10).to_string())

print("\n" + "="*60 + "\n")

# Score baixo (classificação incerta)
suspeitos_3 = df[df["sentimento_score"] < 0.7]
print(f"Score de confiança < 70%: {len(suspeitos_3)}")
print(suspeitos_3[["id", "plataforma", "nota", "sentimento", "sentimento_score", "texto"]].head(10).to_string())