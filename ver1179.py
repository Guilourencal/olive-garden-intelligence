with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1175:1188], 1176):
    print(f'{i}: {line}', end='')
