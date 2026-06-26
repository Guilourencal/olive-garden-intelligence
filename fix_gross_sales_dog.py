content = open('dashboard.py', 'r', encoding='utf-8').read()

old = 'f\'<div style="font-size:13px; font-weight:700; color:#3D2B1F;">R$ {row["gross_sales"]:,.0f}".replace(",",".")</div></div></div>\''
new = 'f\'<div style="font-size:13px; font-weight:700; color:#3D2B1F;">{("R$ {:,.0f}".format(row["gross_sales"])).replace(",",".")}</div></div></div>\''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
