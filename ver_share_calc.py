lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1545:1570], 1546):
    print(f'{i}: {repr(line[:90])}')
