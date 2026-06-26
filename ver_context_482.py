lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[470:485], 471):
    print(f'{i}: {repr(line)}')
