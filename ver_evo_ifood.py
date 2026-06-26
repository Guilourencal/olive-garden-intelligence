lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Evolucao de Receita iFood' in line or 'fig_evo2' in line:
        print(f'{i+1}: {line}', end='')
