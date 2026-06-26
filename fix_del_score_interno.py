lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
del lines[817:897]
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print(f'OK — {len(lines)} linhas')
