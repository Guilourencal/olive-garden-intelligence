content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '@st.cache_data(ttl=300)\ndef carregar_reclamacoes():'
new = '''@st.cache_data(ttl=300)
def carregar_fila_espera():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM fila_espera ORDER BY dia_chegada DESC, hora_chegada DESC", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_reclamacoes():'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK funcao')
else:
    print('TRECHO NAO ENCONTRADO')
