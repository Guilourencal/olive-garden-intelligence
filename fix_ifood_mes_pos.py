content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '                if meses_num_sel and len(meses_num_sel) < 12:\n                    df_if_ytd = df_if_ytd[df_if_ytd["periodo"].str[:2].isin(meses_num_sel)]'
new = '                if meses_num_sel and len(meses_num_sel) < 12:\n                    df_if_ytd = df_if_ytd[df_if_ytd["periodo"].str[3:5].isin(meses_num_sel)]'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
