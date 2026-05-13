with open('atualizar_tudo.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'ifood' in line.lower() or 'coletar_ifood' in line.lower():
        print(f'{i}: {line}', end='')
