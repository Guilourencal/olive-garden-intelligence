with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1190:1202], 1191):
    print(f'{i}: {line}', end='')
