lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Comparativo Mensal' in line or 'comparativo_mensal' in line or '2025' in line and '2026' in line and 'section-title' in line:
        print(f'{i+1}: {line}', end='')
