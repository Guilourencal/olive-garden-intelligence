content = open('dashboard.py', 'r', encoding='utf-8').read()

old = "            # Layout 2x3"
new = "            # Layout 2x3 — grid CSS"

if old in content:
    content = content.replace(old, new, 1)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK marker')
else:
    print('NAO ENCONTRADO')
