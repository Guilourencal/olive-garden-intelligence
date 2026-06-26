import pandas as pd
from db import get_conn
import psycopg2
import os
import glob
from datetime import datetime

PASTA = "data/ifood_reviews"

MAPA_FILIAIS = {
    'OLIVE GARDEN - SHOPPING MORUMBI': 'Olive Garden - Morumbi',
    'OLIVE GARDEN - SHOPPING CENTER NORTE': 'Olive Garden - Center Norte',
    'OLIVE GARDEN - SHOPPING PARQUE DOM PEDRO': 'Olive Garden - Dom Pedro',
    'OLIVE GARDEN - SHOPPING ARICANDUVA': 'Olive Garden - Aricanduva',
    'OLIVE GARDEN - SHOPPING ARICANDUVA (AVENIDA ARICANDUVA)': 'Olive Garden - Aricanduva',
    'OLIVE GARDEN - GUARULHOS GRU2': 'Olive Garden - Guarulhos GRU2',
    'OLIVE GARDEN - GUARULHOS GRU3': 'Olive Garden - Guarulhos GRU3',
    'OLIVE GARDEN  - SHOPPING ARICANDUVA': 'Olive Garden - Aricanduva',
}

def normalizar_filial(nome):
    nome = str(nome).strip().upper()
    for k, v in MAPA_FILIAIS.items():
        if k in nome:
            return v
    return nome.title()

conn = get_conn()
cur = conn.cursor()

arquivos = glob.glob(os.path.join(PASTA, "*.xlsx"))
print(f"Arquivos encontrados: {len(arquivos)}")

total_ins = 0
total_dup = 0

for arquivo in arquivos:
    nome = os.path.basename(arquivo)
    print(f"\nImportando: {nome}")
    
    df = pd.read_excel(arquivo, sheet_name=0, header=0)
    ins = dup = 0
    
    for _, row in df.iterrows():
        try:
            filial = normalizar_filial(str(row.get('Nome da loja', '')))
            nota = float(row.get('Nota', 0)) if pd.notna(row.get('Nota')) else None
            comentario = str(row.get('Comentario', '')) if pd.notna(row.get('Comentario')) else ''
            if comentario == 'nan': comentario = ''
            data_avaliacao = str(row.get('Data da avaliacao', ''))[:10] if pd.notna(row.get('Data da avaliacao')) else ''
            id_pedido = str(row.get('ID longo do pedido', ''))
            
            # Tags positivas
            tags_pos = []
            tags_neg = []
            for col in df.columns:
                if col.startswith('Tag:') and str(row.get(col, 'Nao')) == 'Sim':
                    if col in ['Tag: Comida saborosa','Tag: Bem temperada','Tag: Boa quantidade','Tag: Boa aparencia','Tag: Boa embalagem','Tag: Bons ingredientes','Tag: Temperatura certa','Tag: No ponto certo','Tag: Embalagem sustentavel']:
                        tags_pos.append(col.replace('Tag: ',''))
                    else:
                        tags_neg.append(col.replace('Tag: ',''))
            
            texto = comentario
            if tags_pos: texto += f" [Tags positivas: {', '.join(tags_pos)}]"
            if tags_neg: texto += f" [Tags negativas: {', '.join(tags_neg)}]"
            if not texto.strip(): texto = f"Avaliacao {nota} estrelas"

            cur.execute("SELECT id FROM reviews WHERE fonte_id = %s", (id_pedido,))
            if cur.fetchone():
                dup += 1
                continue
            cur.execute("""
                INSERT INTO reviews (filial, plataforma, nota, texto, data_coleta, fonte_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (filial, 'iFood', nota, texto, datetime.now().strftime('%Y-%m-%d %H:%M'), id_pedido))
            ins += 1
        except Exception as e:
            conn.rollback()
            print(f"  Erro: {e}")
            continue
    
    conn.commit()
    print(f"  Inseridos: {ins} | Duplicatas: {dup}")
    total_ins += ins
    total_dup += dup

cur.execute("SELECT COUNT(id) FROM reviews WHERE plataforma = 'iFood'")
print(f"\nTotal iFood no banco: {cur.fetchone()[0]}")
cur.close()
conn.close()
print("Concluido!")
