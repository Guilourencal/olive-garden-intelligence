content = open('dashboard.py', 'r', encoding='utf-8').read()
content = content.replace('DOURADO', '"#B8923A"')
open('dashboard.py', 'w', encoding='utf-8').write(content)
print(f'OK')
