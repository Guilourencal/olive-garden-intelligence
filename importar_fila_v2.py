import pandas as pd, psycopg2, re
from db import get_conn

df = pd.read_html(r'data\fila_espera\Report_Espera_YTD_Jun16.xls')[0]

def parse_duracao(d):
    if pd.isna(d): return None
    d = str(d).lower().strip()
    h = re.search(r'(\d+)\s*hora', d)
    m = re.search(r'(\d+)\s*minuto', d)
    total = 0
    if h: total += int(h.group(1)) * 60
    if m: total += int(m.group(1))
    return total if total > 0 else None

conn = get_conn()
cur = conn.cursor()

ins = dup = err = 0
for _, row in df.iterrows():
    try:
        duracao = parse_duracao(row.get('Duracao', row.get('Duração')))
        dia_ch = pd.to_datetime(row.get('Dia Chegada'), dayfirst=True).date() if pd.notna(row.get('Dia Chegada')) else None
        dia_fin = pd.to_datetime(row.get('Dia Finalizada'), dayfirst=True).date() if pd.notna(row.get('Dia Finalizada')) else None
        hora_ch = pd.to_datetime(str(row.get('Hora Chegada','')), format='%H:%M', errors='coerce')
        hora_ch = hora_ch.time() if not pd.isna(hora_ch) else None
        hora_fin = pd.to_datetime(str(row.get('Hora Finalizada','')), format='%H:%M', errors='coerce')
        hora_fin = hora_fin.time() if not pd.isna(hora_fin) else None
        pessoas = int(row['Pessoas']) if pd.notna(row.get('Pessoas')) else None
        nome = str(row.get('Nome',''))[:100] if pd.notna(row.get('Nome')) else None
        status = str(row.get('Status',''))[:100] if pd.notna(row.get('Status')) else None
        reg_id = str(row.get('Id',''))[:50] if pd.notna(row.get('Id')) else None

        cur.execute("""
            INSERT INTO fila_espera
            (registro_id, nome, pessoas, dia_chegada, hora_chegada, dia_finalizada, hora_finalizada, duracao_minutos, status, origem, unidade, arquivo_origem)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (registro_id) DO NOTHING
        """, (reg_id, nome, pessoas, dia_ch, hora_ch, dia_fin, hora_fin, duracao, status, 'Restaurant', None, 'Report_Espera_YTD_Jun16.xls'))

        if cur.rowcount > 0: ins += 1
        else: dup += 1
    except Exception as e:
        err += 1

conn.commit()
cur.execute('SELECT COUNT(*), MIN(dia_chegada), MAX(dia_chegada) FROM fila_espera')
r = cur.fetchone()
cur.close()
conn.close()
print(f'Inseridos: {ins} | Duplicatas: {dup} | Erros: {err}')
print(f'Banco: {r[0]} registros | {r[1]} a {r[2]}')
