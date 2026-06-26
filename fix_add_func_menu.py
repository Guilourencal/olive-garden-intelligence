content = open('dashboard.py', 'r', encoding='utf-8').read()

# Adicionar funcao de carregamento
old = '@st.cache_data(ttl=60)\ndef carregar_vendas_diarias():'
new = '''@st.cache_data(ttl=300)
def carregar_menu_analysis():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM menu_analysis ORDER BY semana_ref DESC, gross_sales DESC", conn)
    conn.close()
    return df

@st.cache_data(ttl=60)
def carregar_vendas_diarias():'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK funcao carregamento')
else:
    print('TRECHO NAO ENCONTRADO')
