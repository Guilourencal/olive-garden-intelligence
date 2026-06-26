lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'periodos' in line and ('sort' in line or '=' in line) and 'ifood' in line.lower():
        if 1320 <= i+1 <= 1380:
            print(f'{i+1}: {line}', end='')
