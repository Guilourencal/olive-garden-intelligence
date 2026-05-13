lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'df = carregar_reviews()' in line:
        insert_line = i
        break

nova = []
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
nova.append('')

result = lines[:insert_line] + nova + lines[insert_line:]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result))
print('Feito! Linhas:', len(result))
