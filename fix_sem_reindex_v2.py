content = open('dashboard.py', 'r', encoding='utf-8').read()

old = 'g_ult = g_ult.set_index("dia_norm").reindex(ordem_dias).reset_index()'
new = 'g_ult = g_ult.set_index("dia_norm").reindex([d for d in ordem_dias if d in g_ult["dia_norm"].values]).reset_index()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK reindex ult')
else:
    print('TRECHO NAO ENCONTRADO')

content = open('dashboard.py', 'r', encoding='utf-8').read()

old = 'g_ano1 = g_ano1.set_index("dia_norm").reindex(ordem_dias).reset_index()'
new = 'g_ano1 = g_ano1.set_index("dia_norm").reindex([d for d in ordem_dias if d in g_ano1["dia_norm"].values]).reset_index()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK reindex ano1')
else:
    print('TRECHO NAO ENCONTRADO')
