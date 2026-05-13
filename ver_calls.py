with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'carregar_reviews()' in line or 'carregar_social()' in line or 'carregar_pesquisa' in line:
        if 'def ' not in line:
            print(f'{i}: {line}', end='')
