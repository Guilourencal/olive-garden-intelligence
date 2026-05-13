with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'Cards executivos' in line or 'Visao Executiva' in line:
        print(f'{i}: {line}', end='')
    if 'periodo_sel_v' in line and 'selectbox' in line:
        print(f'{i}: {line}', end='')
