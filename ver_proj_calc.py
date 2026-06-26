lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'proj_restante' in line or 'proj_total' in line:
        if 980 <= i+1 <= 1060:
            print(f'{i+1}: {line}', end='')
