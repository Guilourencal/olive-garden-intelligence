lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1450:1510], 1451):
    print(f'{i}: {line}', end='')
