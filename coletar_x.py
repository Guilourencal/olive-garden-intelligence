from apify_client import ApifyClient
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "apify_api_P1RYuqLAMUsJK8GNblZcnwrThxqQ8v2tL3SZ")

client = ApifyClient(APIFY_TOKEN)

def coletar_x():
    print("Coletando posts e menções do X...")

    run_input = {
        "startUrls": [
            "https://x.com/oLIVe_garden_"
        ],
        "searchTerms": [
            "Olive Garden Brasil",
            "@oLIVe_garden_"
        ],
        "maxItems": 100,
        "sort": "Latest",
        "tweetLanguage": "pt",
    }

    run = client.actor("apidojo/tweet-scraper").call(run_input=run_input)

    itens = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"  {len(itens)} itens retornados")
    if itens:
        print(f"  Campos: {list(itens[0].keys())}")
    return itens


if __name__ == "__main__":
    print("Iniciando coleta X\n")
    itens = coletar_x()