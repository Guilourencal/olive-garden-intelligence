content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''                        fig_dow.add_trace(go.Bar(x=g_ano1["label"], y=g_ano1["venda_salao"], name="Ano Anterior"'''
new = '''                        fig_dow.add_trace(go.Bar(x=g_ano1["label"], y=g_ano1["venda_salao"], name=f"Sem. {num_semana}/{ano_anterior}"'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK label ano anterior')
else:
    print('TRECHO NAO ENCONTRADO')

content = open('dashboard.py', 'r', encoding='utf-8').read()
old = '''name="Semana atual", marker_color=VERDE'''
new = '''name=f"Sem. {num_semana}/{ano_atual}", marker_color=VERDE'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK label semana atual')
else:
    print('TRECHO NAO ENCONTRADO')
