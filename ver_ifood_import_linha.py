lines = open('importar_ifood_vendas.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Importando:' in line and 'arquivo' in line:
        print(f'{i+1}: {repr(line)}')
