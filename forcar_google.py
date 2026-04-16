import psycopg2
import pandas as pd
from transformers import pipeline
import torch
from datetime import datetime

# Classificar sentimento
print("Carregando modelo...")
device = 0 if torch.cuda.is_available() else -1
classificador = pipeline(
    "sentiment-analysis",
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    device=device,
    truncation=True,
    max_length=512,
    local_files_only=True,
)

TEMAS_KEYWORDS = {
    "Atendimento": ["atendimento", "garçom", "garçon", "servidor", "funcionário", "staff", "service", "waiter"],
    "Comida": ["comida", "prato", "massa", "sopa", "salada", "pão", "food", "fresco", "saboroso", "gosto", "sabor"],
    "Preço": ["preço", "caro", "barato", "valor", "custo", "price", "expensive"],
    "Ambiente": ["ambiente", "decoração", "lugar", "espaço", "lindo", "bonito", "atmosphere"],
    "Espera": ["espera", "demora", "rápido", "lento", "tempo", "wait", "fila"],
    "Delivery": ["delivery", "entrega", "ifood", "pedido"],
    "Cardápio": ["cardápio", "menu", "opções", "variedade"],
    "Sobremesas": ["sobremesa", "tiramisu", "gelato", "doce", "dessert"],
}

def classificar_tema(texto):
    if not isinstance(texto, str):
        return "Geral"
    texto_lower = texto.lower()
    temas = []
    for tema, keywords in TEMAS_KEYWORDS.items():
        if any(k in texto_lower for k in keywords):
            temas.append(tema)
    return ", ".join(temas) if temas else "Geral"

df = pd.read_csv("reviews_google_bruto.csv", encoding="utf-8-sig")
print(f"Classificando {len(df)} reviews...")

sentimentos = []
for texto in df["texto"].tolist():
    if not isinstance(texto, str) or not texto.strip():
        sentimentos.append({"sentimento": "Neutro", "score": 0.0})
        continue
    try:
        saida = classificador([texto])[0]
        label = saida["label"].lower()
        score = round(saida["score"], 3)
        if "positive" in label:
            sentimentos.append({"sentimento": "Positivo", "score": score})
        elif "negative" in label:
            sentimentos.append({"sentimento": "Negativo", "score": score})
        else:
            sentimentos.append({"sentimento": "Neutro", "score": score})
    except:
        sentimentos.append({"sentimento": "Neutro", "score": 0.0})

df["sentimento"] = [s["sentimento"] for s in sentimentos]
df["sentimento_score"] = [s["score"] for s in sentimentos]
df["tema"] = df["texto"].apply(classificar_tema)

print(f"\nDistribuição:")
print(df["sentimento"].value_counts().to_string())

# Inserir no banco
conn = psycopg2.connect(
    host="aws-1-sa-east-1.pooler.supabase.com",
    port=6543,
    user="postgres.rvauallshhozpruvusrr",
    password="olivegarden2233@",
    database="postgres"
)
cur = conn.cursor()

# Normalizar nomes das filiais
nomes_map = {
    "Olive Garden - GRU2": "Olive Garden - Guarulhos GRU2",
    "Olive Garden - GRU3": "Olive Garden - Guarulhos GRU3",
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
cur.execute("SELECT COUNT(*) FROM reviews WHERE plataforma = 'Google Reviews'")
print(f"\nTotal Google no banco: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM reviews")
print(f"Total geral: {cur.fetchone()[0]}")
cur.close()
conn.close()
print("Concluído!")