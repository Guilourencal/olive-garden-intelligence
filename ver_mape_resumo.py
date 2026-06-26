import psycopg2
from db import get_conn
import pandas as pd

conn = get_conn()
df = pd.read_sql("SELECT data_alvo, filial, erro_pct FROM projecoes_historico WHERE valor_realizado IS NOT NULL AND erro_pct IS NOT NULL ORDER BY data_alvo", conn)
conn.close()
df['filial'] = df['filial'].str.replace('Olive Garden - ','')
df['data_alvo'] = pd.to_datetime(df['data_alvo'])
print(f'Total amostras: {len(df)} | Periodo: {df["data_alvo"].min().date()} a {df["data_alvo"].max().date()}')
print()
print('=== MAPE POR FILIAL ===')
for filial, grp in df.groupby('filial'):
    mape = grp['erro_pct'].abs().mean()
    bias = grp['erro_pct'].mean()
    print(f'  {filial}: MAPE={mape:.1f}% | Bias={bias:+.1f}% | n={len(grp)}')
print()
print('=== EVOLUCAO SEMANAL ===')
df['semana'] = df['data_alvo'].dt.to_period('W').astype(str)
por_semana = df.groupby('semana').agg(mape=('erro_pct', lambda x: x.abs().mean()), bias=('erro_pct','mean'), n=('erro_pct','count')).reset_index()
for _, row in por_semana.iterrows():
    print(f'  {row["semana"]}: MAPE={row["mape"]:.1f}% | Bias={row["bias"]:+.1f}% | n={int(row["n"])}')
