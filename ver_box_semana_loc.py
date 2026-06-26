lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Ultima Semana Fechada' in line or 'col_r2' in line:
        if 1100 <= i+1 <= 1300:
            print(f'{i+1}: {line}', end='')
