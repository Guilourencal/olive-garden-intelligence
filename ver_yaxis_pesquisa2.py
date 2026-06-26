lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'range' in line and ('80' in line or '60' in line or '100' in line) and 'yaxis' in line:
        if 880 <= i+1 <= 1050:
            print(f'{i+1}: {line}', end='')
