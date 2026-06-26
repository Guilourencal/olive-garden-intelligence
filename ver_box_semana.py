lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Ultima Semana' in line or 'ultima_semana' in line or 'semana' in line.lower():
        if 1050 <= i+1 <= 1200:
            print(f'{i+1}: {line}', end='')
