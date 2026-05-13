import pandas as pd

print('Lendo amostra da aba Dados...')
df = pd.read_excel('data/dash_vendas.xlsx', sheet_name='Dados', header=0, nrows=5000)
df['data_parse'] = pd.to_datetime(df['dia'], errors='coerce')
print(f'Anos disponiveis: {df["ANO"].dropna().unique()}')
print(f'Datas validas: {df["data_parse"].notna().sum()}')
print(f'Range de datas: {df["data_parse"].min()} a {df["data_parse"].max()}')
print(f'Primeiras linhas com ANO 2025:')
df25 = df[df['ANO'] == 2025]
print(f'  {len(df25)} linhas com ANO=2025')
print(df25[['restaurante','dia','ANO','VENDA TOTAL']].head(5).to_string())
