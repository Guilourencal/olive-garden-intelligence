content = open('dashboard.py', 'r', encoding='utf-8').read()

old = 'df_fila = carregar_fila_espera()'
new = 'df_fila = carregar_fila_espera()\ndf_ifood_diario = carregar_ifood_diario()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK df')
else:
    print('TRECHO NAO ENCONTRADO')
