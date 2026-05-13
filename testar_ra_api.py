import requests
import json

url = "https://iosearch.reclameaqui.com.br/raichu-io-site-search-v1/query/companyComplains/0/10"
params = {
    "company": "olive-garden",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.reclameaqui.com.br/",
}
r = requests.get(url, params=params, headers=headers)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
else:
    print(r.text[:500])
