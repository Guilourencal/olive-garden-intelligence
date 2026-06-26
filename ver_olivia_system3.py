lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1720:1745], 1721):
    print(f'{i}: {repr(line[:100])}')
