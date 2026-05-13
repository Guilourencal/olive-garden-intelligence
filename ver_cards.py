with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[967:1002], 968):
    print(f'{i}: {line}', end='')
