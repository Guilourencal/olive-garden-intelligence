lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Ano Anterior' in line or 'ano_anterior' in line or 'W-1' in line or 'semana' in line.lower():
        if 1050 <= i+1 <= 1300:
            print(f'{i+1}: {line}', end='')
