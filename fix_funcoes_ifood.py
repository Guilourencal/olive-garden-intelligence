lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'def carregar_pesquisa_performance():' in line:
        insert_line = i + 5
        break

nova = []
nova.append('')
nova.append('@st.cache_data(ttl=300)')
nova.append('def carregar_ifood_vendas():')
nova.append('    conn = get_conn()')
nova.append('    df = pd.read_sql("SELECT * FROM ifood_vendas ORDER BY periodo, filial", conn)')
nova.append('    conn.close()')
nova.append('    return df')
nova.append('')
nova.append('@st.cache_data(ttl=300)')
nova.append('def carregar_ifood_horarios():')
nova.append('    conn = get_conn()')
nova.append('    df = pd.read_sql("SELECT * FROM ifood_horarios", conn)')
nova.append('    conn.close()')
nova.append('    return df')
nova.append('')
nova.append('@st.cache_data(ttl=300)')
nova.append('def carregar_ifood_pagamentos():')
nova.append('    conn = get_conn()')
nova.append('    df = pd.read_sql("SELECT * FROM ifood_pagamentos", conn)')
nova.append('    conn.close()')
nova.append('    return df')
nova.append('')
nova.append('@st.cache_data(ttl=300)')
nova.append('def carregar_ifood_dias():')
nova.append('    conn = get_conn()')
nova.append('    df = pd.read_sql("SELECT * FROM ifood_dias", conn)')
nova.append('    conn.close()')
nova.append('    return df')

result = lines[:insert_line] + nova + lines[insert_line:]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result))
print(f'Inserido apos linha {insert_line}. Total: {len(result)} linhas')
