lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1585:1615], 1586):
    print(f'{i}: {repr(line[:90])}')
