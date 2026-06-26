import pandas as pd
import os

pasta = r'data\ifood_vendas'
for f in os.listdir(pasta):
    if '14' in f:
        caminho = os.path.join(pasta, f)
        xl = pd.ExcelFile(caminho)
        print(f'Arquivo: {f}')
        print(f'Abas: {xl.sheet_names}')
        df = pd.read_excel(caminho, sheet_name=xl.sheet_names[0], nrows=5)
        print(df.head(2).to_string())
        print()
