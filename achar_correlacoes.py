with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'Correlacoes' in line and 'aba_sel' in line and 'elif' in line:
        print(f'{i}: {line}', end='')
    if 'OlivIA' in line and 'aba_sel' in line and 'elif' in line:
        print(f'{i}: {line}', end='')
