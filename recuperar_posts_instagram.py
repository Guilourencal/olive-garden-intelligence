from apify_client import ApifyClient
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "apify_api_P1RYuqLAMUsJK8GNblZcnwrThxqQ8v2tL3SZ")

client = ApifyClient(APIFY_TOKEN)

print("Recuperando posts do run anterior...")
run = client.run("kpeCtte3nAXl5kmKS").get()
posts = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"  {len(posts)} posts encontrados")

dados = []
for p in posts:
    dados.append({
        "url": p.get("url", ""),
        "shortCode": p.get("shortCode", ""),
        "displayUrl": p.get("displayUrl", ""),
        "caption": p.get("caption", "")[:100] if p.get("caption") else "",
        "likesCount": p.get("likesCount", 0),
        "commentsCount": p.get("commentsCount", 0),
        "timestamp": p.get("timestamp", ""),
    })

df = pd.DataFrame(dados)
df.to_csv("social_instagram_posts.csv", index=False, encoding="utf-8-sig")
print(f"Posts salvos: {len(df)}")
print(df[["url", "displayUrl"]].head(3).to_string())