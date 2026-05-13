with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'OlivIA' in line or 'Olivia' in line or 'olivia' in line:
        print(f'{i}: {line}', end='')
