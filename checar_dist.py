import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)

df = pd.read_sql("SELECT nota, sentimento, texto FROM reviews", conn)
conn.close()

print("Distribuição geral:")
print(df["sentimento"].value_counts())
print(f"\nNota média: {df['nota'].mean():.2f}")

print("\nReviews com nota >= 4 mas Negativo:")
err1 = df[(df["nota"] >= 4) & (df["sentimento"] == "Negativo")]
print(f"Total: {len(err1)}")
for _, r in err1.iterrows():
    print(f"  Nota {r['nota']} | {r['texto'][:80]}")

print("\nReviews com nota <= 2 mas Positivo:")
err2 = df[(df["nota"] <= 2) & (df["sentimento"] == "Positivo")]
print(f"Total: {len(err2)}")
for _, r in err2.iterrows():
    print(f"  Nota {r['nota']} | {r['texto'][:80]}")