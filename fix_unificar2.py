novo = '''import pandas as pd
import psycopg2
import glob
import os

# Google — CSV
google = pd.read_csv("reviews_google_bruto.csv", encoding="utf-8-sig")
print(f"Google: {len(google)} reviews")
print(f"  Primeiro: {google['texto'].iloc[0][:60]}")

# TripAdvisor — CSV
tripadvisor = pd.read_csv("reviews_tripadvisor_bruto.csv", encoding="utf-8-sig")
print(f"TripAdvisor: {len(tripadvisor)} reviews")

# iFood — lendo direto dos arquivos Excel oficiais
MAPA_FILIAIS = {
    'OLIVE GARDEN - SHOPPING MORUMBI': 'Olive Garden - Morumbi',
    'OLIVE GARDEN - SHOPPING CENTER NORTE': 'Olive Garden - Center Norte',
    'OLIVE GARDEN - SHOPPING PARQUE DOM PEDRO': 'Olive Garden - Dom Pedro',
    'OLIVE GARDEN - SHOPPING ARICANDUVA': 'Olive Garden - Aricanduva',
    'OLIVE GARDEN  - SHOPPING ARICANDUVA': 'Olive Garden - Aricanduva',
    'OLIVE GARDEN - GUARULHOS GRU2': 'Olive Garden - Guarulhos GRU2',
    'OLIVE GARDEN - GUARULHOS GRU3': 'Olive Garden - Guarulhos GRU3',
}

def normalizar_filial(nome):
    nome = str(nome).strip().upper()
    for k, v in MAPA_FILIAIS.items():
        if k in nome:
            return v
    return nome.title()

arquivos_ifood = glob.glob("data/ifood_reviews/*.xlsx")
ifood_rows = []
ids_vistos = set()
for arquivo in arquivos_ifood:
    df_if = pd.read_excel(arquivo, sheet_name=0, header=0)
    for _, row in df_if.iterrows():
        id_pedido = str(row.get('ID longo do pedido', ''))
        if id_pedido in ids_vistos:
            continue
        ids_vistos.add(id_pedido)
        filial = normalizar_filial(str(row.get('Nome da loja', '')))
        nota = float(row.get('Nota', 0)) if pd.notna(row.get('Nota')) else None
        comentario = str(row.get('Comentario', '')) if pd.notna(row.get('Comentario')) else ''
        if comentario == 'nan': comentario = ''
        data_av = str(row.get('Data da avaliacao', ''))[:10] if pd.notna(row.get('Data da avaliacao')) else ''
        tags_pos = []
        tags_neg = []
        for col in df_if.columns:
            if col.startswith('Tag:') and str(row.get(col, 'Nao')) == 'Sim':
                if col in ['Tag: Comida saborosa','Tag: Bem temperada','Tag: Boa quantidade','Tag: Boa aparencia','Tag: Boa embalagem','Tag: Bons ingredientes','Tag: Temperatura certa','Tag: No ponto certo','Tag: Embalagem sustentavel']:
                    tags_pos.append(col.replace('Tag: ',''))
                else:
                    tags_neg.append(col.replace('Tag: ',''))
        texto = comentario
        if tags_pos: texto += f" [Tags positivas: {', '.join(tags_pos)}]"
        if tags_neg: texto += f" [Tags negativas: {', '.join(tags_neg)}]"
        if not texto.strip(): texto = f"Avaliacao {nota} estrelas"
        ifood_rows.append({"filial": filial, "plataforma": "iFood", "nota": nota, "texto": texto, "autor": "", "data_original": data_av, "data_coleta": data_av})

ifood = pd.DataFrame(ifood_rows) if ifood_rows else pd.DataFrame(columns=["filial","plataforma","nota","texto","autor","data_original","data_coleta"])
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
print(f"\\nTotal unificado: {len(df)}")
print(f"\\nPor plataforma:")
print(df["plataforma"].value_counts().to_string())
print(f"\\nFiliais:")
print(df["filial"].value_counts().to_string())
'''
open('unificar_dados.py', 'w', encoding='utf-8').write(novo)
print('Feito!')
