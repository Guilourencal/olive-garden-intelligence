lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[616:680], 617):
    print(f'{i}: {line}', end='')
