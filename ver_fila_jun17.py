import pandas as pd

df = pd.read_html(r'data\fila_espera\Report_Espera_YTD_Jun17.xls')[0]
print(f'Total registros no arquivo: {len(df)}')
print(f'Range datas: {df["Dia Chegada"].min()} a {df["Dia Chegada"].max()}')
print(f'Registros jun 15-17:')
jun_novo = df[df['Dia Chegada'].isin(['15/06/2026','16/06/2026','17/06/2026'])]
print(f'  {len(jun_novo)} registros')
print(jun_novo[['Dia Chegada','Status','Pessoas']].head(10).to_string())
