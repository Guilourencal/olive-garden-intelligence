lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'data_ini' in line or 'data_fim' in line or 'periodo_sel' in line:
        if 980 <= i+1 <= 1060:
            print(f'{i+1}: {line}', end='')
