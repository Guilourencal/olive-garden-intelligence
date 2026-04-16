import pandas as pd
from transformers import pipeline
import torch
import psycopg2
from datetime import datetime

print("Carregando modelo de sentimento...")
device = 0 if torch.cuda.is_available() else -1
classificador = pipeline(
    "sentiment-analysis",
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    device=device,
    truncation=True,
    max_length=512,
)

def classificar_sentimento(textos):
    resultados = []
    for texto in textos:
        if not isinstance(texto, str) or not texto.strip():
            resultados.append({"sentimento": "Neutro", "score": 0.0})
            continue
        try:
            saida = classificador([texto])[0]
            label = saida["label"].lower()
            score = round(saida["score"], 3)
            if "positive" in label:
                sentimento = "Positivo"
            elif "negative" in label:
                sentimento = "Negativo"
            else:
                sentimento = "Neutro"
            resultados.append({"sentimento": sentimento, "score": score})
        except:
            resultados.append({"sentimento": "Neutro", "score": 0.0})
    return resultados

print("Carregando comentários do Instagram...")
df = pd.read_csv("social_instagram_bruto.csv", encoding="utf-8-sig")
print(f"  {len(df)} comentários")

print("Classificando sentimento...")
resultados = classificar_sentimento(df["texto"].tolist())
df["sentimento"] = [r["sentimento"] for r in resultados]
df["sentimento_score"] = [r["score"] for r in resultados]

df.to_csv("social_instagram_classificado.csv", index=False, encoding="utf-8-sig")
print(f"\nDistribuição de sentimento:")
print(df["sentimento"].value_counts().to_string())

print("\nCriando tabela no banco...")
conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS social (
        id SERIAL PRIMARY KEY,
        rede VARCHAR(50),
        post_url TEXT,
        autor VARCHAR(255),
        texto TEXT,
        likes INTEGER,
        respostas INTEGER,
        sentimento VARCHAR(50),
        sentimento_score FLOAT,
        data_original VARCHAR(100),
        data_coleta VARCHAR(50),
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(autor, texto, rede)
    )
""")
conn.commit()
print("Tabela 'social' criada!")

inseridos = 0
for _, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO social (rede, post_url, autor, texto, likes, respostas,
                sentimento, sentimento_score, data_original, data_coleta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (autor, texto, rede) DO NOTHING
        """, (
            row.get("rede"), row.get("post_url"), row.get("autor"),
            row.get("texto"), row.get("likes"), row.get("respostas"),
            row.get("sentimento"), row.get("sentimento_score"),
            row.get("data_original"), row.get("data_coleta")
        ))
        inseridos += 1
    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")

conn.commit()
cur.execute("SELECT COUNT(*) FROM social")
print(f"\nTotal no banco: {cur.fetchone()[0]}")
cur.close()
conn.close()
print("Concluído!")