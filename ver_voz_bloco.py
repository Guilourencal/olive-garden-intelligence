lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[466:490], 467):
    print(f'{i}: {repr(line[:90])}')
