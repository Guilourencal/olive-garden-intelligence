lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'def carregar_ifood_tags():' in line:
        insert_line = i + 5
        break

nova = [
    '',
    '@st.cache_data(ttl=300)',
    'def carregar_vendas_diarias():',
    '    conn = get_conn()',
    '    df = pd.read_sql("SELECT * FROM vendas_diarias ORDER BY data, filial", conn)',
    '    conn.close()',
    '    return df',
]

result = lines[:insert_line] + nova + lines[insert_line:]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result))
print(f'Funcao inserida! Total: {len(result)} linhas')
