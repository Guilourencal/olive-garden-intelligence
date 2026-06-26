content = open('dashboard.py', 'r', encoding='utf-8').read()

old = 'df_menu = carregar_menu_analysis()'
new = 'df_menu = carregar_menu_analysis()\ndf_reclamacoes = carregar_reclamacoes()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK df')
else:
    print('TRECHO NAO ENCONTRADO')
