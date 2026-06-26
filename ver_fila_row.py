import pandas as pd
import re

df = pd.read_html(r'data\fila_espera\Report_Espera_YTD_Jun16.xls')[0]
row = df.iloc[0]
print('Campos da primeira linha:')
for col in df.columns:
    print(f'  {col}: {repr(row[col])}')
