with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1162:1180], 1163):
    print(f'{i}: {line}', end='')
