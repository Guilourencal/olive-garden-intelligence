content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '@st.cache_data(ttl=300)\ndef carregar_fila_espera():'
new = '''@st.cache_data(ttl=300)
def carregar_ifood_diario():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ifood_diario ORDER BY data", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_fila_espera():'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK funcao')
else:
    print('TRECHO NAO ENCONTRADO')
