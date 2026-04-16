import requests
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "d221918a842342d19f9635d9e1f26bcd")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "1deab88afe74c92b1a581854e9088e73")

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def buscar_gnews(q, lang, label, max_results=10):
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": q,
        "lang": lang,
        "max": max_results,
        "apikey": GNEWS_API_KEY,
        "sortby": "publishedAt",
    }
    r = requests.get(url, params=params)
    data = r.json()
    artigos = data.get("articles", [])
    resultados = []
    for a in artigos:
        titulo = a.get("title", "") or ""
        if not titulo or titulo == "[Removed]":
            continue
        resultados.append({
            "categoria": label,
            "titulo": titulo,
            "descricao": a.get("description", "") or "",
            "fonte": a.get("source", {}).get("name", ""),
            "url": a.get("url", ""),
            "imagem": a.get("image", ""),
            "publicado_em": a.get("publishedAt", ""),
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
    return resultados

def buscar_newsapi(q, lang, label, obrigatorio):
    data_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    try:
        resultado = newsapi.get_everything(
            q=q,
            language=lang,
            from_param=data_inicio,
            sort_by="publishedAt",
            page_size=20,
        )
        artigos = resultado.get("articles", [])
        resultados = []
        for a in artigos:
            titulo = a.get("title", "") or ""
            descricao = a.get("description", "") or ""
            if not titulo or titulo == "[Removed]":
                continue
            texto = f"{titulo} {descricao}".lower()
            if not any(kw in texto for kw in obrigatorio):
                continue
            resultados.append({
                "categoria": label,
                "titulo": titulo,
                "descricao": descricao,
                "fonte": a.get("source", {}).get("name", ""),
                "url": a.get("url", ""),
                "imagem": a.get("urlToImage", ""),
                "publicado_em": a.get("publishedAt", ""),
                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
        return resultados
    except Exception as e:
        print(f"  Erro NewsAPI: {e}")
        return []

def coletar_noticias():
    print("Coletando notícias...\n")
    todas = []

    # GNews — Olive Garden Global
    print("GNews: Olive Garden Global...")
    artigos = buscar_gnews("Olive Garden restaurant", "en", "Olive Garden Global", 10)
    print(f"  {len(artigos)} artigos")
    todas.extend(artigos)

    # GNews — Olive Garden Brasil
    print("GNews: Olive Garden Brasil...")
    artigos = buscar_gnews("Olive Garden Brasil", "pt", "Olive Garden Brasil", 10)
    print(f"  {len(artigos)} artigos")
    todas.extend(artigos)

    # GNews — Mercado A&B Global
    print("GNews: Mercado A&B Global...")
    artigos = buscar_gnews("restaurant industry food service dining", "en", "Mercado A&B Global", 10)
    print(f"  {len(artigos)} artigos")
    todas.extend(artigos)

    # NewsAPI — Mercado A&B Brasil
    print("NewsAPI: Mercado A&B Brasil...")
    artigos = buscar_newsapi(
        q="food service brasil restaurantes ABRASEL",
        lang="pt",
        label="Mercado A&B Brasil",
        obrigatorio=["food service", "restaurante", "abrasel", "foodservice", "alimentação"]
    )
    print(f"  {len(artigos)} artigos")
    todas.extend(artigos)

    if todas:
        df = pd.DataFrame(todas)
        df = df.drop_duplicates(subset=["url"])
        df = df[df["titulo"].notna()]
        df.to_csv("noticias_bruto.csv", index=False, encoding="utf-8-sig")
        print(f"\nTotal de notícias: {len(df)}")
        print(f"\nPor categoria:")
        print(df["categoria"].value_counts().to_string())
        print(f"\nTítulos:")
        for _, row in df.iterrows():
            print(f"  [{row['categoria']}] {row['titulo'][:80]}")
    else:
        print("\nNenhuma notícia coletada.")

if __name__ == "__main__":
    coletar_noticias()