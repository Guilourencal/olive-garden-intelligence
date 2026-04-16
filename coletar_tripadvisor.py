from apify_client import ApifyClient
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "apify_api_P1RYuqLAMUsJK8GNblZcnwrThxqQ8v2tL3SZ")

FILIAIS = [
    {"url": "https://www.tripadvisor.com.br/Restaurant_Review-g303605-d15003200-Reviews-Olive_Garden-Campinas_State_of_Sao_Paulo.html", "nome": "Olive Garden - Campinas"},
    {"url": "https://www.tripadvisor.com.br/Restaurant_Review-g303611-d6989450-Reviews-Olive_Garden-Guarulhos_State_of_Sao_Paulo.html", "nome": "Olive Garden - Guarulhos GRU2"},
    {"url": "https://www.tripadvisor.com.br/Restaurant_Review-g303611-d19823306-Reviews-Olive_Garden-Guarulhos_State_of_Sao_Paulo.html", "nome": "Olive Garden - Guarulhos GRU3"},
    {"url": "https://www.tripadvisor.com.br/Restaurant_Review-g303631-d12253895-Reviews-Olive_Garden_Shopping_Center_Norte-Sao_Paulo_State_of_Sao_Paulo.html", "nome": "Olive Garden - Center Norte"},
    {"url": "https://www.tripadvisor.com.br/Restaurant_Review-g303631-d13314027-Reviews-Olive_Garden_Shopping_Morumbi-Sao_Paulo_State_of_Sao_Paulo.html", "nome": "Olive Garden - Morumbi"},
    {"url": "https://www.tripadvisor.com.br/Restaurant_Review-g303631-d15236153-Reviews-Olive_Garden_Shopping_Aricanduva-Sao_Paulo_State_of_Sao_Paulo.html", "nome": "Olive Garden - Aricanduva"},
]

client = ApifyClient(APIFY_TOKEN)

def coletar_reviews_tripadvisor(url, nome_filial):
    print(f"Coletando: {nome_filial}")

    run_input = {
        "query": [url],
        "reviewsPerPlace": 20,
        "parseAllReviews": False,
        "sortBy": "most_recent",
        "locale": "pt-BR",
    }

    run = client.actor("api-ninja/tripadvisor-reviews-scraper").call(run_input=run_input)

    reviews = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        autor = item.get("reviewer", {})
        if isinstance(autor, dict):
            autor = autor.get("name", "")
        reviews.append({
            "filial": nome_filial,
            "plataforma": "TripAdvisor",
            "autor": autor,
            "nota": item.get("rating"),
            "texto": item.get("text", ""),
            "data_original": item.get("published_at_date", ""),
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "nota_geral_filial": None,
            "total_avaliacoes_filial": None,
        })

    print(f"  {len(reviews)} reviews coletados")
    return reviews


if __name__ == "__main__":
    print("Iniciando coleta TripAdvisor — todas as filiais\n")

    todos_os_reviews = []

    for filial in FILIAIS:
        reviews = coletar_reviews_tripadvisor(filial["url"], filial["nome"])
        todos_os_reviews.extend(reviews)

    if todos_os_reviews:
        df = pd.DataFrame(todos_os_reviews)
        df.to_csv("reviews_tripadvisor_bruto.csv", index=False, encoding="utf-8-sig")
        print(f"\nTotal de reviews salvos: {len(df)}")
        print(f"Filiais coletadas: {df['filial'].nunique()}")
        print(f"\nResumo por filial:")
        print(df.groupby("filial")["nota"].agg(["count", "mean"]).round(2).to_string())
    else:
        print("\nNenhum review coletado.")