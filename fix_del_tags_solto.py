lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
del lines[481:499]
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
