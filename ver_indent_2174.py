lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[2170:2180], 2171):
    print(f'{i}: {repr(line)}')
