lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'def carregar_' in line:
        print(f'{i+1}: {line}', end='')
