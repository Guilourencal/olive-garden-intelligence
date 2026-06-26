lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'visao_sel == "iFood"' in line or 'iFood' in line and 'section-title' in line:
        print(f'{i+1}: {line}', end='')
