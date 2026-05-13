with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'fig_rank_v' in line and 'plotly_chart' in line:
        print(f'{i}: {line}', end='')
    if 'r=160' in line:
        print(f'{i}: {line}', end='')
