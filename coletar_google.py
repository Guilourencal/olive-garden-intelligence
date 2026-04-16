import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBEcXlQ4HvPMdOHIH7yZufwh20YxzXPDec")

FILIAIS = [
    {"place_id": "ChIJx4XhvZBYzpQRsStcbe81j8E", "nome": "Olive Garden - Center Norte"},
    {"place_id": "ChIJ2yulQ8NQzpQR8AKZDe1rgNA", "nome": "Olive Garden - Morumbi"},
    {"place_id": "ChIJVasWclBnzpQRBkIRun9RmFU", "nome": "Olive Garden - Aricanduva"},
    {"place_id": "ChIJbeK1sT_1zpQRZ6SjCagzQVg", "nome": "Olive Garden - GRU3"},
    {"place_id": "ChIJ06sArDCLzpQROh4NzQZ3LD4", "nome": "Olive Garden - GRU2"},
    {"place_id": "ChIJH4hbbz7HyJQRfeyVGRZjR5M", "nome": "Olive Garden - Dom Pedro"},
]


def buscar_reviews(place_id, nome_filial):
    url = f"https://places.googleapis.com/v1/places/{place_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "displayName,rating,userRatingCount,reviews",
    }
    params = {
        "languageCode": "pt-BR"
    }
    resposta = requests.get(url, headers=headers, params=params)
    dados = resposta.json()

    if "error" in dados:
        print(f"  Erro na API: {dados['error'].get('message', 'desconhecido')}")
        return []

    reviews_brutos = dados.get("reviews", [])
    nota_geral = dados.get("rating")
    total_avaliacoes = dados.get("userRatingCount")

    print(f"  Nota geral: {nota_geral} ({total_avaliacoes} avaliações) — {len(reviews_brutos)} reviews coletados")

    reviews_limpos = []
    for r in reviews_brutos:
        texto = r.get("text", {}).get("text", "")
        autor = r.get("authorAttribution", {}).get("displayName", "")
        reviews_limpos.append({
            "filial": nome_filial,
            "plataforma": "Google Reviews",
            "autor": autor,
            "nota": r.get("rating"),
            "texto": texto,
            "data_original": r.get("relativePublishTimeDescription", ""),
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "nota_geral_filial": nota_geral,
            "total_avaliacoes_filial": total_avaliacoes,
        })

    return reviews_limpos


if __name__ == "__main__":
    print("Iniciando coleta Google Reviews — todas as filiais\n")

    todos_os_reviews = []

    for filial in FILIAIS:
        print(f"Coletando: {filial['nome']}")
        reviews = buscar_reviews(filial["place_id"], filial["nome"])
        todos_os_reviews.extend(reviews)

    if todos_os_reviews:
        df = pd.DataFrame(todos_os_reviews)
        df.to_csv("reviews_google_bruto.csv", index=False, encoding="utf-8-sig")

        print(f"\nColeta finalizada.")
        print(f"Total de reviews salvos: {len(df)}")
        print(f"Filiais coletadas com sucesso: {df['filial'].nunique()}")
        print(f"\nResumo por filial:")
        print(df.groupby("filial")["nota"].agg(["count", "mean"]).round(2).to_string())
    else:
        print("\nNenhum review coletado. Verifique os Place IDs e a chave de API.")