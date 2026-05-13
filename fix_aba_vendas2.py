lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'fix_ifood_calls.py' in line and 'aba_sel' in line:
        lines[i] = 'elif aba_sel == "Vendas":'
        print(f'Linha {i+1} corrigida!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
