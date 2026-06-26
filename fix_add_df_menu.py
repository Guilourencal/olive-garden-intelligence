content = open('dashboard.py', 'r', encoding='utf-8').read()

old = 'df_vendas_diarias = carregar_vendas_diarias()'
new = '''df_vendas_diarias = carregar_vendas_diarias()
df_menu = carregar_menu_analysis()'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
