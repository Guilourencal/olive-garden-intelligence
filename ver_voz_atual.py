lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[471:490], 472):
    print(f'{i}: {repr(line[:90])}')
