with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1085:1120], 1086):
    print(f'{i}: {line}', end='')
