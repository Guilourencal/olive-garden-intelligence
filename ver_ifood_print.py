lines = open('importar_ifood_vendas.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'print' in line and ('Importando' in line or 'arquivo' in line.lower()):
        print(f'{i+1}: {repr(line)}')
