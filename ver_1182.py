with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 1170 <= i <= 1195:
        print(f'{i}: {line}', end='')
