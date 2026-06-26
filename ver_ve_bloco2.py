lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1170:1225], 1171):
    print(f'{i}: {repr(line[:100])}')
