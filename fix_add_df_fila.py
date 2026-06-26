content = open('dashboard.py', 'r', encoding='utf-8').read()

old = 'df_reclamacoes = carregar_reclamacoes()'
new = 'df_reclamacoes = carregar_reclamacoes()\ndf_fila = carregar_fila_espera()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK df')
else:
    print('TRECHO NAO ENCONTRADO')
