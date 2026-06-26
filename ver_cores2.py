lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[:80]):
    if '=' in line and ('#' in line or 'color' in line.lower()):
        print(f'{i+1}: {line}', end='')
