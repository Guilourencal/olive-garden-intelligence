lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'df_perf = carregar_pesquisa_performance()' in line:
        insert_line = i + 1
        break

nova = []
nova.append('df_ifood_vendas = carregar_ifood_vendas()')
nova.append('df_ifood_horarios = carregar_ifood_horarios()')
nova.append('df_ifood_pagamentos = carregar_ifood_pagamentos()')
nova.append('df_ifood_dias = carregar_ifood_dias()')

result = lines[:insert_line] + nova + lines[insert_line:]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result))
print(f'Inserido apos linha {insert_line}. Total: {len(result)} linhas')
