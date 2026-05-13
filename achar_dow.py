with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'Media de Venda por Dia da Semana' in line:
        print(f'{i}: {line}', end='')
    if 'fig_dow_vd' in line and 'plotly_chart' in line:
        print(f'{i}: {line}', end='')
