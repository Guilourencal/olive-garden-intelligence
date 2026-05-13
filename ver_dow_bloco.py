with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1163:1205], 1164):
    print(f'{i}: {line}', end='')
