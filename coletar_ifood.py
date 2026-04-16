from apify_client import ApifyClient
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "apify_api_P1RYuqLAMUsJK8GNblZcnwrThxqQ8v2tL3SZ")

FILIAIS = [
    {"store_id": "15f69e93-409d-4507-a8d6-625689cfcdb9", "nome": "Olive Garden - Morumbi"},
    {"store_id": "c3c202c5-ca2c-46d2-a1ce-2f7a202596cc", "nome": "Olive Garden - Aricanduva"},
    {"store_id": "856f126b-ed19-41f8-9ee7-487f8d1d7205", "nome": "Olive Garden - Center Norte"},
    {"store_id": "18ae4a8c-7887-4bd5-9dab-9d40ff8a9be0", "nome": "Olive Garden - Dom Pedro"},
]

client = ApifyClient(APIFY_TOKEN)

def coletar_reviews_ifood(store_id, nome_filial):
    print(f"Coletando: {nome_filial}")

    run_input = {
        "mode": "reviews",
        "store_id": store_id,
    }

    run = client.actor("yasmany.casanova/ifood-scraper").call(run_input=run_input)

    reviews = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        data = item.get("data", {})
        reviews_brutos = data.get("reviews", [])
        for r in reviews_brutos:
            reviews.append({
                "filial": nome_filial,
                "plataforma": "iFood",
                "autor": r.get("customer_name", ""),
                "nota": r.get("rating"),
                "texto": r.get("comment", ""),
                "data_original": r.get("comment_date", ""),
                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "nota_geral_filial": None,
                "total_avaliacoes_filial": data.get("total_reviews_available"),
            })

    print(f"  {len(reviews)} reviews coletados")
    return reviews


if __name__ == "__main__":
    print("Iniciando coleta iFood — todas as filiais\n")

    todos_os_reviews = []

    for filial in FILIAIS:
        reviews = coletar_reviews_ifood(filial["store_id"], filial["nome"])
        todos_os_reviews.extend(reviews)

    if todos_os_reviews:
        df = pd.DataFrame(todos_os_reviews)
        df = df[df["texto"].notna() & (df["texto"].str.strip() != "")]
        df.to_csv("reviews_ifood_bruto.csv", index=False, encoding="utf-8-sig")
        print(f"\nTotal de reviews salvos: {len(df)}")
        print(f"Filiais coletadas: {df['filial'].nunique()}")
        print(f"\nResumo por filial:")
        print(df.groupby("filial")["nota"].agg(["count", "mean"]).round(2).to_string())
    else:
        print("\nNenhum review coletado.")