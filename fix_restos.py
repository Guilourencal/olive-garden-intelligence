lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
del lines[1179:1185]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('Feito!')
