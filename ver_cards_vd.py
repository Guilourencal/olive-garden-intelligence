with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'delta_html' in line and 'cor_d' in line:
        print(f'{i}: {line}', end='')
