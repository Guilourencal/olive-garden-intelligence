from apify_client import ApifyClient
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "apify_api_P1RYuqLAMUsJK8GNblZcnwrThxqQ8v2tL3SZ")

client = ApifyClient(APIFY_TOKEN)

print("Recuperando comentários do run anterior...")

run = client.run("fOz5ceZ9pHAaQ2LLf").get()
comentarios = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"  {len(comentarios)} comentários encontrados")

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
    print(f"Total de comentários salvos: {len(df)}")
    print(f"\nPrimeiros 3:")
    print(df[["autor", "texto"]].head(3).to_string())
else:
    print("Nenhum comentário com texto encontrado.")