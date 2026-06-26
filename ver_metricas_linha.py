lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[895:910], 896):
    print(f'{i}: {line}', end='')
