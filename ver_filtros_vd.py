lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'df_vd_f' in line and ('filter' in line.lower() or '=' in line):
        if 960 <= i+1 <= 1010:
            print(f'{i+1}: {line}', end='')
