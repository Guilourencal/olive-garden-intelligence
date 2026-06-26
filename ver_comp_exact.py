content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '            df_2025 = df_mensal[df_mensal["ano"]==2025].groupby(["mes_num","mes_label"])["venda_sala'
new = '            df_2025 = df_mensal[df_mensal["ano"]==2025].groupby(["mes_num","mes_label"])["venda_sala'

# Vamos ver o trecho exato
print(repr(content[content.find('df_2025 = df_mensal'):content.find('df_2025 = df_mensal')+200]))
