import psycopg2
from db import get_conn
import pandas as pd
import os
import re

conn = get_conn()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS fila_espera (
        id SERIAL PRIMARY KEY,
        registro_id VARCHAR(50) UNIQUE,
        nome VARCHAR(100),
        pessoas INTEGER,
        dia_chegada DATE,
        hora_chegada TIME,
        dia_finalizada DATE,
        hora_finalizada TIME,
        duracao_minutos INTEGER,
        status VARCHAR(100),
        origem VARCHAR(50),
        unidade VARCHAR(100),
        arquivo_origem VARCHAR(255)
    )
""")
conn.commit()
print('Tabela criada!')

def parse_duracao(d):
    if pd.isna(d): return None
    d = str(d).lower().strip()
    h = re.search(r'(\d+)\s*hora', d)
    m = re.search(r'(\d+)\s*minuto', d)
    total = 0
    if h: total += int(h.group(1)) * 60
    if m: total += int(m.group(1))
    return total if total > 0 else None

pasta = r'data\fila_espera'
os.makedirs(pasta, exist_ok=True)
arquivos = [f for f in os.listdir(pasta) if f.endswith('.xls') or f.endswith('.xlsx')]
print(f'Arquivos encontrados: {len(arquivos)}')

total_ins = total_dup = total_err = 0
for arquivo in sorted(arquivos):
    caminho = os.path.join(pasta, arquivo)
    print(f'\nImportando: {arquivo}')
    try:
        dfs = pd.read_html(caminho)
        df = dfs[0]
    except:
        df = pd.read_excel(caminho)

    # Detectar unidade pelo nome do arquivo
    unidade = None
    for u in ['Morumbi','Center Norte','Dom Pedro','Aricanduva','GRU2','GRU3']:
        if u.lower().replace(' ','') in arquivo.lower().replace(' ',''):
            unidade = u
            break

    ins = dup = err = 0
    for _, row in df.iterrows():
        try:
            duracao = parse_duracao(row.get('Duração', row.get('Duracao')))
            dia_ch = pd.to_datetime(row.get('Dia Chegada'), dayfirst=True).date() if pd.notna(row.get('Dia Chegada')) else None
            dia_fin = pd.to_datetime(row.get('Dia Finalizada'), dayfirst=True).date() if pd.notna(row.get('Dia Finalizada')) else None
            hora_ch_raw = row.get('Hora Chegada')
            hora_fin_raw = row.get('Hora Finalizada')
            hora_ch = pd.to_datetime(str(hora_ch_raw), format='%H:%M', errors='coerce').time() if pd.notna(hora_ch_raw) else None
            hora_fin = pd.to_datetime(str(hora_fin_raw), format='%H:%M', errors='coerce').time() if pd.notna(hora_fin_raw) else None
            pessoas = int(row['Pessoas']) if pd.notna(row.get('Pessoas')) else None
            nome = str(row.get('Nome',''))[:100] if pd.notna(row.get('Nome')) else None
            status = str(row.get('Status',''))[:100] if pd.notna(row.get('Status')) else None
            reg_id = str(row.get('Id',''))[:50] if pd.notna(row.get('Id')) else None

            cur.execute("""
                INSERT INTO fila_espera
                (registro_id, nome, pessoas, dia_chegada, hora_chegada, dia_finalizada, hora_finalizada, duracao_minutos, status, origem, unidade, arquivo_origem)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (registro_id) DO NOTHING
            """, (reg_id, nome, pessoas, dia_ch, hora_ch, dia_fin, hora_fin, duracao, status, 'Restaurant', unidade, arquivo))

            if cur.rowcount > 0: ins += 1
            else: dup += 1
        except Exception as e:
            err += 1
            continue

    conn.commit()
    print(f'  Inseridos: {ins} | Duplicatas: {dup} | Erros: {err}')
    total_ins += ins; total_dup += dup; total_err += err

cur.execute('SELECT COUNT(*), MIN(dia_chegada), MAX(dia_chegada) FROM fila_espera')
r = cur.fetchone()
print(f'\nBanco: {r[0]} registros | {r[1]} a {r[2]}')
cur.close()
conn.close()
print('Concluido!')
