import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql("""
    SELECT filial, periodo, horario, pedidos, faturamento
    FROM ifood_horarios
    WHERE periodo LIKE '%05/2026%'
    ORDER BY filial, horario
""", conn)
conn.close()

print('=== HORARIOS DISPONIVEIS MAIO 2026 ===')
print('Horarios unicos:', sorted(df['horario'].unique()))
print()
print('Total registros:', len(df))
print()

# Classificar almoco (11-15h) vs jantar (17-22h)
df['hora'] = df['horario'].str.extract(r'(\d+)h').astype(float)
df['turno'] = df['hora'].apply(lambda h: 'Almoco' if 11<=h<=15 else 'Jantar' if 17<=h<=22 else 'Outros')

print('=== FATURAMENTO POR TURNO — MAIO MTD ===')
resumo = df.groupby('turno').agg(
    faturamento=('faturamento','sum'),
    pedidos=('pedidos','sum')
).reset_index()
resumo['ticket_medio'] = (resumo['faturamento'] / resumo['pedidos']).round(0)
resumo['pct_fat'] = (resumo['faturamento'] / resumo['faturamento'].sum() * 100).round(1)
print(resumo.to_string(index=False))

print()
print('=== POR FILIAL E TURNO ===')
por_filial = df.groupby(['filial','turno']).agg(
    faturamento=('faturamento','sum'),
    pedidos=('pedidos','sum')
).reset_index()
por_filial['filial'] = por_filial['filial'].str.replace('Olive Garden - ','')
por_filial['ticket'] = (por_filial['faturamento']/por_filial['pedidos']).round(0)
print(por_filial.to_string(index=False))
