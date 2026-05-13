lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
lines[1097] = '            gc_fmt = f"{int(gc):,}".replace(",", ".")'
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('Feito!')
