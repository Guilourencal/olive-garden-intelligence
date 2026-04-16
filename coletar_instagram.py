from apify_client import ApifyClient
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "apify_api_P1RYuqLAMUsJK8GNblZcnwrThxqQ8v2tL3SZ")

client = ApifyClient(APIFY_TOKEN)

def coletar_posts():
    print("Coletando posts do @olivegardenbr...")
    run_input = {
        "directUrls": ["https://www.instagram.com/olivegardenbr/"],
        "resultsType": "posts",
        "resultsLimit": 20,
        "addParentData": False,
    }
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    posts = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"  {len(posts)} posts coletados")
    return posts

def coletar_comentarios(posts):
    print("Coletando comentários...")
    urls_posts = [p.get("url") for p in posts if p.get("url")]
    if not urls_posts:
        print("  Nenhuma URL encontrada")
        return []

    run_input = {
        "directUrls": urls_posts[:20],
        "resultsType": "comments",
        "resultsLimit": 50,
        "addParentData": True,
    }
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    comentarios = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"  {len(comentarios)} comentários coletados")
    return comentarios

def processar_e_salvar(comentarios):
    dados = []
    for c in comentarios:
        texto = c.get("text", "")
        if not texto or not texto.strip():
            continue
        dados.append({
            "rede": "Instagram",
            "post_url": c.get("postUrl", ""),
            "autor": c.get("ownerUsername", ""),
            "texto": texto,
            "likes": c.get("likesCount", 0),
            "respostas": c.get("repliesCount", 0),
            "data_original": c.get("timestamp", ""),
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    if dados:
        df = pd.DataFrame(dados)
        df.to_csv("social_instagram_bruto.csv", index=False, encoding="utf-8-sig")
        print(f"\nTotal de comentários salvos: {len(df)}")
        print(f"\nPrimeiros 3 comentários:")
        print(df[["autor", "texto"]].head(3).to_string())
    else:
        print("\nNenhum comentário com texto encontrado.")


if __name__ == "__main__":
    print("Iniciando coleta Instagram\n")
    posts = coletar_posts()
    if posts:
        comentarios = coletar_comentarios(posts)
        processar_e_salvar(comentarios)