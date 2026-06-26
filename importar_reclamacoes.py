import psycopg2
from db import get_conn
import pandas as pd
import os

conn = get_conn()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS reclamacoes_buzzmonitor (
        id SERIAL PRIMARY KEY,
        data DATE NOT NULL,
        comentario TEXT,
        canal VARCHAR(50),
        sentimento VARCHAR(20),
        avaliacao FLOAT,
        unidade VARCHAR(100),
        unidade_curta VARCHAR(50),
        tema VARCHAR(100),
        subtema VARCHAR(100),
        categorias_raw TEXT,
        arquivo_origem VARCHAR(255),
        UNIQUE(data, comentario, unidade)
    )
""")
conn.commit()
print('Tabela criada!')

pasta = r'data\reclamacoes'
os.makedirs(pasta, exist_ok=True)
arquivos = [f for f in os.listdir(pasta) if f.endswith('.xlsx') or f.endswith('.xls')]
print(f'Arquivos encontrados: {len(arquivos)}')

UNIDADE_MAP = {
    'OG_Shopping Morumbi': 'Morumbi',
    'OG_Shopping Center Norte': 'Center Norte',
    'OG_Parque Dom Pedro': 'Dom Pedro',
    'OG_Shopping Aricanduva': 'Aricanduva',
    'OG_Aeroporto GRU T3': 'Guarulhos GRU3',
    'OG_Aeroporto GRU T2': 'Guarulhos GRU2',
}

total_ins = total_dup = 0
for arquivo in sorted(arquivos):
    caminho = os.path.join(pasta, arquivo)
    print(f'\nImportando: {arquivo}')
    df = pd.read_excel(caminho)
    df.columns = [c.strip() for c in df.columns]
    ins = dup = 0
    for _, row in df.iterrows():
        unidade_raw = str(row.get('UNIDADE','')) if pd.notna(row.get('UNIDADE')) else ''
        unidade_curta = UNIDADE_MAP.get(unidade_raw, unidade_raw)
        cats_raw = str(row.get('Reclamacao', row.get('Reclamação',''))) if pd.notna(row.get('Reclamacao', row.get('Reclamação',''))) else ''
        cats = [c.strip() for c in cats_raw.split(',') if c.strip()]
        tema = None
        subtema = None
        if cats:
            partes = cats[0].split('_')
            tema = partes[1] if len(partes) > 1 else None
            subtema = partes[2] if len(partes) > 2 else None
        try:
            cur.execute("""
                INSERT INTO reclamacoes_buzzmonitor
                (data, comentario, canal, sentimento, avaliacao, unidade, unidade_curta, tema, subtema, categorias_raw, arquivo_origem)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (data, comentario, unidade) DO NOTHING
            """, (
                row.get('DATA'),
                str(row.get('COMENTÁRIO', row.get('COMENTARIO','')))[:2000] if pd.notna(row.get('COMENTÁRIO', row.get('COMENTARIO',''))) else None,
                str(row.get('CANAL','')) if pd.notna(row.get('CANAL')) else None,
                str(row.get('SENTIMENTO','')) if pd.notna(row.get('SENTIMENTO')) else None,
                float(row['AVALIAÇÃO']) if pd.notna(row.get('AVALIAÇÃO', row.get('AVALIACAO'))) else None,
                unidade_raw, unidade_curta,
                tema, subtema, cats_raw, arquivo
            ))
            if cur.rowcount > 0:
                ins += 1
            else:
                dup += 1
        except Exception as e:
            conn.rollback()
            print(f'  Erro: {e}')
            continue
    conn.commit()
    print(f'  Inseridos: {ins} | Duplicatas: {dup}')
    total_ins += ins
    total_dup += dup

cur.execute('SELECT COUNT(*), MIN(data), MAX(data) FROM reclamacoes_buzzmonitor')
row = cur.fetchone()
print(f'\nBanco: {row[0]} registros | {row[1]} a {row[2]}')
cur.close()
conn.close()
print('Concluido!')
