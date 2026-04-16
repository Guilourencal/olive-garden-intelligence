import requests

API_KEY = "1deab88afe74c92b1a581854e9088e73"

buscas = [
    {"q": "Olive Garden", "lang": "en", "label": "Olive Garden Global"},
    {"q": "Olive Garden Brasil", "lang": "pt", "label": "Olive Garden Brasil"},
    {"q": "food service brasil restaurantes", "lang": "pt", "label": "Mercado A&B Brasil"},
    {"q": "WOW Restaurants", "lang": "pt", "label": "WOW Restaurants"},
]

for busca in buscas:
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": busca["q"],
        "lang": busca["lang"],
        "max": 10,
        "apikey": API_KEY,
        "sortby": "publishedAt",
    }
    r = requests.get(url, params=params)
    data = r.json()
    artigos = data.get("articles", [])
    print(f"\n{busca['label']} — {busca['q']}: {len(artigos)} artigos")
    for a in artigos:
        print(f"  [{a.get('source', {}).get('name', '')}] {a.get('title', '')[:70]}")