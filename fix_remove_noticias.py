lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'for aba in' in line and 'Noti' in line:
        lines[i] = '    for aba in ["Reviews", "Social", "Pesquisa", "Correlacoes", "OlivIA"]:'
        print(f'Linha {i+1} atualizada!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
