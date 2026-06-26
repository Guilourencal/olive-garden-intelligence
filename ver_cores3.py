lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[80:130], 81):
    if '=' in line and '#' in line and len(line) < 60:
        print(f'{i}: {line}', end='')
