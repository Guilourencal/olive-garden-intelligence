lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'importar_ifood_vendas' in line and 'for aba in' in line:
        lines[i] = '    for aba in ["Reviews", "Social", "Pesquisa", "Correlacoes", "Vendas", "OlivIA"]:'
        print(f'Linha {i+1} corrigida!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
