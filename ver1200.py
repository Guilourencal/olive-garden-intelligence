with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1195:1210], 1196):
    print(f'{i}: {line}', end='')
