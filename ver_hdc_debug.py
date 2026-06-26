import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql("""
    SELECT filial, data, venda_salao, hdc, venda_por_hdc
    FROM vendas_diarias
    WHERE EXTRACT(month FROM data)=6 AND EXTRACT(year FROM data)=2026
    ORDER BY filial, data
""", conn)
conn.close()

df['filial'] = df['filial'].str.replace('Olive Garden - ','')
print('=== DADOS JUNHO 2026 ===')
print(f'Registros: {len(df)}')
print()
resumo = df.groupby('filial').agg(
    venda=('venda_salao','sum'),
    hdc_medio=('hdc','mean'),
    venda_hdc_media=('venda_por_hdc','mean'),
    dias=('data','count')
).reset_index()
print(resumo.to_string(index=False))
print()
print('=== AMOSTRA HDC ===')
print(df[['filial','data','venda_salao','hdc','venda_por_hdc']].head(12).to_string(index=False))
