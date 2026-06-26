content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '@st.cache_data(ttl=60)\ndef carregar_vendas_diarias():'
new = '''@st.cache_data(ttl=300)
def carregar_reclamacoes():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM reclamacoes_buzzmonitor ORDER BY data DESC", conn)
    conn.close()
    return df

@st.cache_data(ttl=60)
def carregar_vendas_diarias():'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK funcao')
else:
    print('TRECHO NAO ENCONTRADO')
