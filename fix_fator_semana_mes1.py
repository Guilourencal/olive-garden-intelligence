content = open('aprender_modelo.py', 'r', encoding='utf-8').read()

old = '    fator_dow = dff_c.groupby(\'dow\')[\'venda_salao\'].mean() / media\n    fator_mes = dff_c.groupby(\'mes\')[\'venda_salao\'].mean() / media'
new = '    fator_dow = dff_c.groupby(\'dow\')[\'venda_salao\'].mean() / media\n    fator_mes = dff_c.groupby(\'mes\')[\'venda_salao\'].mean() / media\n    # Fator semana do mes (S1=dias 1-7, S2=8-14, S3=15-21, S4=22-31)\n    dff_c[\'semana_mes\'] = dff_c[\'data\'].dt.day.apply(lambda d: 1 if d<=7 else 2 if d<=14 else 3 if d<=21 else 4)\n    fator_semana_mes = dff_c.groupby(\'semana_mes\')[\'venda_salao\'].mean() / media'

if old in content:
    content = content.replace(old, new)
    open('aprender_modelo.py', 'w', encoding='utf-8').write(content)
    print('OK fatores')
else:
    print('TRECHO NAO ENCONTRADO')
