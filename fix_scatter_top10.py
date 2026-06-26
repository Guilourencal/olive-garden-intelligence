content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '        df_scatter = df_mf[df_mf["revenue_score"].notna() & df_mf["number_of_checks"].notna()].copy()'
new = '        df_scatter = df_mf[df_mf["revenue_score"].notna() & df_mf["number_of_checks"].notna()].copy()\n        df_scatter = df_scatter.sort_values("revenue_score", ascending=False).head(10)'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
