lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'Ranking por filial' in line and '#' in line:
        start = i
        print(f'Inicio encontrado: linha {i+1}')
    if 'fig_rank_v' in line and 'plotly_chart' in line:
        end = i
        print(f'Fim encontrado: linha {i+1}')
        break
