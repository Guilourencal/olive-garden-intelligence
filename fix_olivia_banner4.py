lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if 'with open("static/' in l and 'olivia' in l.lower())
lines[idx] = '    with open("static/olivia_banner_final.png", "rb") as _f:\n'
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
