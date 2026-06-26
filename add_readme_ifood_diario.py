with open('README_ROTINAS.md', 'a', encoding='utf-8') as f:
    f.write('''
### Atualizar iFood (diario):
`powershell
# 1. Salvar arquivo mensal acumulado em data\\ifood_vendas\\
python importar_ifood_vendas.py

# 2. Salvar arquivo diario em data\\ifood_diario\\
python importar_ifood_diario.py
`
''')
print('OK')
