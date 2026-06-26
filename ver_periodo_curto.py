lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'periodo_curto' in line or 'FW' in line:
        if 880 <= i+1 <= 1000:
            print(f'{i+1}: {line}', end='')
