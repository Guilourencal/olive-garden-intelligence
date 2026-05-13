with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1178:1202], 1179):
    print(f'{i}: {line}', end='')
