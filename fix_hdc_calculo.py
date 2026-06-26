content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '            df_hdc = df_mes_hdc.groupby("filial_curta").agg(venda_por_hdc=("venda_por_hdc","mean"), venda_salao=("venda_salao","sum")).reset_index()'
new = '            df_hdc = df_mes_hdc.groupby("filial_curta").agg(venda_salao=("venda_salao","sum"), hdc=("hdc","mean")).reset_index()\n            df_hdc["venda_por_hdc"] = (df_hdc["venda_salao"] / df_hdc["hdc"]).round(0)'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
