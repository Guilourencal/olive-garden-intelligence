import pandas as pd
import psycopg2
import glob
import os
from datetime import datetime

PASTA = "data/ifood_reviews"

MAPA_FILIAIS = {
    'OLIVE GARDEN - SHOPPING MORUMBI': 'Olive Garden - Morumbi',
    'OLIVE GARDEN - SHOPPING CENTER NORTE': 'Olive Garden - Center Norte',
    'OLIVE GARDEN - SHOPPING PARQUE DOM PEDRO': 'Olive Garden - Dom Pedro',
    'OLIVE GARDEN - SHOPPING ARICANDUVA': 'Olive Garden - Aricanduva',
    'OLIVE GARDEN  - SHOPPING ARICANDUVA': 'Olive Garden - Aricanduva',
    'OLIVE GARDEN - GUARULHOS GRU2': 'Olive Garden - Guarulhos GRU2',
    'OLIVE GARDEN - GUARULHOS GRU3': 'Olive Garden - Guarulhos GRU3',
}

TAGS_POSITIVAS = [
    'Tag: Comida saborosa', 'Tag: Bem temperada', 'Tag: Boa quantidade',
    'Tag: Boa aparência', 'Tag: Boa embalagem', 'Tag: Bons ingredientes',
    'Tag: Temperatura certa', 'Tag: No ponto certo', 'Tag: Embalagem sustentável'
]
TAGS_NEGATIVAS = [
    'Tag: Pedido incompleto', 'Tag: Itens vieram errados',
    'Tag: Itens danificados', 'Tag: Mal embalado'
]

def normalizar_filial(nome):
    nome = str(nome).strip().upper()
    for k, v in MAPA_FILIAIS.items():
        if k in nome:
            return v
    return nome.title()

conn = psycopg2.connect(
    host='aws-1-sa-east-1.pooler.supabase.com',
    port=6543,
    user='postgres.rvauallshhozpruvusrr',
    password='olivegarden2233@',
    database='postgres'
)
cur = conn.cursor()

arquivos = glob.glob(os.path.join(PASTA, "*.xlsx"))
print(f"Arquivos encontrados: {len(arquivos)}")

for arquivo in arquivos:
    nome = os.path.basename(arquivo)
    print(f"\nImportando tags: {nome}")
    df = pd.read_excel(arquivo, sheet_name=0, header=0)
    
    # Extrair periodo do arquivo
    datas = df['Data da avaliação'].dropna()
    if len(datas) > 0:
        data_min = pd.to_datetime(datas).min().strftime('%d/%m/%Y')
        data_max = pd.to_datetime(datas).max().strftime('%d/%m/%Y')
        periodo = f"{data_min} - {data_max}"
    else:
        periodo = nome[:20]
    
    ins = dup = 0
    for filial_orig in df['Nome da loja'].unique():
        filial = normalizar_filial(str(filial_orig))
        df_fil = df[df['Nome da loja'] == filial_orig]
        total = len(df_fil)
        
        all_tags = [(t, 'positiva') for t in TAGS_POSITIVAS] + [(t, 'negativa') for t in TAGS_NEGATIVAS]
        for tag, tipo in all_tags:
            if tag not in df_fil.columns:
                continue
            sim = (df_fil[tag] == 'Sim').sum()
            nao = (df_fil[tag] == 'Não').sum()
            pct = float(round(float(sim) / total * 100, 1)) if total > 0 else 0.0
            tag_label = tag.replace('Tag: ', '')
            try:
                cur.execute("""
                    INSERT INTO ifood_tags (periodo, filial, tag, tipo, total_sim, total_nao, pct_sim)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (periodo, filial, tag) DO UPDATE
                    SET total_sim=%s, total_nao=%s, pct_sim=%s
                """, (periodo, filial, tag_label, tipo, int(sim), int(nao), pct, int(sim), int(nao), pct))
                ins += 1
            except Exception as e:
                conn.rollback()
                print(f"  Erro: {e}")
                dup += 1
    
    conn.commit()
    print(f"  Tags inseridas/atualizadas: {ins} | Erros: {dup}")

cur.execute("SELECT COUNT(id) FROM ifood_tags")
print(f"\nTotal ifood_tags: {cur.fetchone()[0]}")
cur.close()
conn.close()
print("Concluido!")
