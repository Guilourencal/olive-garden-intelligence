from apify_client import ApifyClient
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "apify_api_P1RYuqLAMUsJK8GNblZcnwrThxqQ8v2tL3SZ")

client = ApifyClient(APIFY_TOKEN)

def coletar_reclameaqui():
    print("Coletando: Olive Garden - Reclame Aqui")

    run_input = {
        "companies": ["olive-garden"],
        "maxComplaints": 100,
        "statusFilter": "all",
        "includeCompanyStats": True,
    }

    run = client.actor("viralanalyzer/reclameaqui-scraper").call(run_input=run_input)

    reviews = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        reviews.append(item)

    print(f"  {len(reviews)} itens retornados")
    if reviews:
        print(f"  Campos disponíveis: {list(reviews[0].keys())}")
    return reviews


if __name__ == "__main__":
    print("Iniciando coleta Reclame Aqui\n")
    itens = coletar_reclameaqui()