import pandas as pd

df = pd.read_csv("reviews_unificado.csv", encoding="utf-8-sig")
print(f"Total: {len(df)}")
print(f"\nPor plataforma:")
print(df["plataforma"].value_counts().to_string())
print(f"\nPrimeiros 3 Google:")
google = df[df["plataforma"] == "Google Reviews"]["texto"].head(3)
print(google.to_string())