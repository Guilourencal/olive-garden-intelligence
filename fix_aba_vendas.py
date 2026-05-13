lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'aba_sel ==' in line and 'importar_ifood' in line:
        lines[i] = 'elif aba_sel == "Vendas":'
        print(f'Linha {i+1} corrigida!')
        break
    if 'aba_sel ==' in line and 'fix_nome_aba.py$' in line:
        lines[i] = 'elif aba_sel == "Vendas":'
        print(f'Linha {i+1} corrigida!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
