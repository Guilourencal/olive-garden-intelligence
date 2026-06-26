content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '                    system=OLIVIA_SYSTEM,'
new = '                    system=OLIVIA_SYSTEM + _contexto_dinamico,'

count = content.count(old)
content = content.replace(old, new)
open('dashboard.py', 'w', encoding='utf-8').write(content)
print(f'OK — {count} ocorrencias substituidas')
