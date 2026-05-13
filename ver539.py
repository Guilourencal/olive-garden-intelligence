with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[528:545], 529):
    print(f'{i}: {line}', end='')
