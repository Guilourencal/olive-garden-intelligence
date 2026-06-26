import pandas as pd, psycopg2, re
from db import get_conn

df = pd.read_html(r'data\fila_espera\Report_Espera_YTD_Jun16.xls')[0]
row = df.iloc[0]

def parse_duracao(d):
    if pd.isna(d): return None
    d = str(d).lower().strip()
    h = re.search(r'(\d+)\s*hora', d)
    m = re.search(r'(\d+)\s*minuto', d)
    total = 0
    if h: total += int(h.group(1)) * 60
    if m: total += int(m.group(1))
    return total if total > 0 else None

duracao = parse_duracao(row.get('Duracao', row.get('Duração')))
dia_ch = pd.to_datetime(row.get('Dia Chegada'), dayfirst=True).date()
dia_fin = pd.to_datetime(row.get('Dia Finalizada'), dayfirst=True).date()
hora_ch = pd.to_datetime(str(row.get('Hora Chegada')), format='%H:%M', errors='coerce').time()
hora_fin = pd.to_datetime(str(row.get('Hora Finalizada')), format='%H:%M', errors='coerce').time()
pessoas = int(row['Pessoas'])
nome = str(row.get('Nome',''))[:100]
status = str(row.get('Status',''))[:100]
reg_id = str(row.get('Id',''))[:50]

vals = (reg_id, nome, pessoas, dia_ch, hora_ch, dia_fin, hora_fin, duracao, 'Restaurant', None, 'Report_Espera_YTD_Jun16.xls')
print('Valores a inserir:')
for i, v in enumerate(vals):
    print(f'  [{i}] {repr(v)}')

conn = get_conn()
cur = conn.cursor()
try:
    cur.execute("""
        INSERT INTO fila_espera
        (registro_id, nome, pessoas, dia_chegada, hora_chegada, dia_finalizada, hora_finalizada, duracao_minutos, status, origem, unidade, arquivo_origem)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (registro_id) DO NOTHING
    """, vals)
    conn.commit()
    print('OK inserido!')
except Exception as e:
    print('ERRO:', e)
cur.close()
conn.close()
