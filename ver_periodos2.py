lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'periodos' in line and '=' in line:
        if 1320 <= i+1 <= 1380:
            print(f'{i+1}: {line}', end='')
