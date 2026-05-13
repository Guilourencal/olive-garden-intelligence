lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if '"Reviews", "Social", "Noticias", "Pesquisa", "OlivIA"' in line or '"Reviews", "Social", "Not' in line:
        lines[i] = '    for aba in ["Reviews", "Social", "Noticias", "Pesquisa", "Correlacoes", "OlivIA"]:'
        print(f'Linha {i+1} atualizada!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
