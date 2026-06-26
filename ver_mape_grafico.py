import psycopg2
from db import get_conn
import pandas as pd
import numpy as np

conn = get_conn()
df = pd.read_sql("""
    SELECT data_alvo, filial, erro_pct
    FROM projecoes_historico
    WHERE valor_realizado IS NOT NULL AND erro_pct IS NOT NULL
    ORDER BY data_alvo
""", conn)
conn.close()

print('Total amostras:', len(df))
print('Periodo:', df['data_alvo'].min(), 'a', df['data_alvo'].max())
print()
por_dia = df.groupby('data_alvo').agg(
    mape=('erro_pct', lambda x: x.abs().mean()),
    bias=('erro_pct', 'mean'),
    n=('erro_pct', 'count')
).reset_index()
print(por_dia.to_string(index=False))
