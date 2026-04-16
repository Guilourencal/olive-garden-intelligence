import pandas as pd
from transformers import pipeline
import torch
from LeIA import SentimentIntensityAnalyzer
from datetime import datetime

print("Carregando modelo de sentimento...")
device = 0 if torch.cuda.is_available() else -1
classificador = pipeline(
    "sentiment-analysis",
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    device=device,
    truncation=True,
    max_length=512,
    local_files_only=True,
)

analisador_leia = SentimentIntensityAnalyzer()

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

def sentimento_por_nota(nota):
    if pd.isna(nota):
        return "Neutro"
    if nota >= 4:
        return "Positivo"
    elif nota <= 2:
        return "Negativo"
    return "Neutro"

def classificar_sentimento_hibrido(texto, nota):
    if not isinstance(texto, str) or not texto.strip():
        return sentimento_por_nota(nota), 0.0

    # Textos muito curtos — usa nota
    if len(texto.split()) < 5:
        return sentimento_por_nota(nota), 0.5

    # BERTimbau
    try:
        saida = classificador([texto])[0]
        label = saida["label"].lower()
        score_bert = round(saida["score"], 3)
        if "positive" in label:
            sent_bert = "Positivo"
        elif "negative" in label:
            sent_bert = "Negativo"
        else:
            sent_bert = "Neutro"
    except:
        sent_bert = sentimento_por_nota(nota)
        score_bert = 0.5

    # LeIA
    try:
        scores_leia = analisador_leia.polarity_scores(texto)
        compound = scores_leia["compound"]
        if compound >= 0.05:
            sent_leia = "Positivo"
        elif compound <= -0.05:
            sent_leia = "Negativo"
        else:
            sent_leia = "Neutro"
    except:
        sent_leia = sentimento_por_nota(nota)

    # Decisão final
    if sent_bert == sent_leia:
        return sent_bert, score_bert

    # Divergência — nota como árbitro
    sent_nota = sentimento_por_nota(nota)

    # Se nota concorda com um dos dois, usa esse
    if sent_nota == sent_bert:
        return sent_bert, score_bert
    elif sent_nota == sent_leia:
        return sent_leia, abs(compound)
    else:
        # Nota é neutra e os dois divergem — usa BERTimbau se score alto
        if score_bert >= 0.7:
            return sent_bert, score_bert
        return sent_nota, 0.5


print("Carregando reviews...")
df = pd.read_csv("reviews_unificado.csv", encoding="utf-8-sig")
print(f"Total: {len(df)} reviews")

print("Classificando sentimento híbrido...")
resultados = []
for i, row in df.iterrows():
    sent, score = classificar_sentimento_hibrido(row.get("texto", ""), row.get("nota"))
    resultados.append({"sentimento": sent, "sentimento_score": score})
    if (i + 1) % 20 == 0:
        print(f"  Progresso: {i+1}/{len(df)}")

df["sentimento"] = [r["sentimento"] for r in resultados]
df["sentimento_score"] = [r["sentimento_score"] for r in resultados]
df["tema"] = df["texto"].apply(classificar_tema)

df.to_csv("reviews_classificado.csv", index=False, encoding="utf-8-sig")

print(f"\nDistribuição de sentimento:")
print(df["sentimento"].value_counts().to_string())
print(f"\nSentimento por plataforma:")
print(df.groupby(["plataforma", "sentimento"]).size().unstack(fill_value=0).to_string())