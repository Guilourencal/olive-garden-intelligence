import psycopg2
from db import get_conn
import pandas as pd
import numpy as np

conn = get_conn()
df = pd.read_sql("""
    SELECT filial, data_projecao, data_alvo, valor_projetado, valor_realizado, erro_pct
    FROM projecoes_historico
    WHERE valor_realizado IS NOT NULL
    ORDER BY filial, data_alvo
""", conn)
conn.close()

print('=== EVOLUCAO DOS MAPEs POR FILIAL ===')
print()
for filial in sorted(df['filial'].unique()):
    dff = df[df['filial']==filial].copy()
    print(filial + ':')
    for _, row in dff.iterrows():
        sinal = '+' if row['erro_pct'] > 0 else ''
        print('  ' + str(row['data_alvo']) + ' | Proj: R$' + str(round(row['valor_projetado'])) + ' | Real: R$' + str(round(row['valor_realizado'])) + ' | Erro: ' + sinal + str(round(row['erro_pct'],1)) + '%')
    mape = dff['erro_pct'].abs().mean()
    bias = dff['erro_pct'].mean()
    print('  MAPE=' + str(round(mape,1)) + '% | Bias=' + str(round(bias,1)) + '% | n=' + str(len(dff)))
    print()

print('=== RESUMO GERAL ===')
print('MAPE geral: ' + str(round(df['erro_pct'].abs().mean(),1)) + '%')
print('Bias geral: ' + str(round(df['erro_pct'].mean(),1)) + '%')
print('Total amostras: ' + str(len(df)))
print()
print('=== EVOLUCAO DIARIA DA REDE ===')
por_data = df.groupby('data_alvo').agg(
    mape=('erro_pct', lambda x: x.abs().mean()),
    bias=('erro_pct', 'mean'),
    n=('erro_pct', 'count')
).reset_index()
for _, row in por_data.iterrows():
    print('  ' + str(row['data_alvo']) + ': MAPE=' + str(round(row['mape'],1)) + '% | Bias=' + str(round(row['bias'],1)) + '% | n=' + str(int(row['n'])) + ' filiais')
