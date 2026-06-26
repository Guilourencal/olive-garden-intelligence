lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1175:1210], 1176):
    print(f'{i}: {repr(line[:80])}')
