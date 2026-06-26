content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '        df_rev = df_reviews.copy()'
new = '        df_rev = df.copy()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
