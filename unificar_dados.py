import pandas as pd

# Google — CSV novo com reviews em português
google = pd.read_csv("reviews_google_bruto.csv", encoding="utf-8-sig")
print(f"Google: {len(google)} reviews")
print(f"  Primeiro: {google['texto'].iloc[0][:60]}")

# TripAdvisor
tripadvisor = pd.read_csv("reviews_tripadvisor_bruto.csv", encoding="utf-8-sig")
print(f"TripAdvisor: {len(tripadvisor)} reviews")

# iFood
ifood = pd.read_csv("reviews_ifood_bruto.csv", encoding="utf-8-sig")
print(f"iFood: {len(ifood)} reviews")

# Unifica
df = pd.concat([google, tripadvisor, ifood], ignore_index=True)

# Normaliza filiais
nomes_map = {
    "Olive Garden - GRU2": "Olive Garden - Guarulhos GRU2",
    "Olive Garden - GRU3": "Olive Garden - Guarulhos GRU3",
    "Olive Garden - Campinas": "Olive Garden - Dom Pedro",
}
df["filial"] = df["filial"].replace(nomes_map)

df.to_csv("reviews_unificado.csv", index=False, encoding="utf-8-sig")
print(f"\nTotal unificado: {len(df)}")
print(f"\nPor plataforma:")
print(df["plataforma"].value_counts().to_string())
print(f"\nFiliais:")
print(df["filial"].value_counts().to_string())