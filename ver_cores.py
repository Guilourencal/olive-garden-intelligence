lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'DOURADO' in line or 'MARROM' in line or 'VERDE' in line or 'VERMELHO' in line:
        if i+1 <= 50:
            print(f'{i+1}: {line}', end='')
