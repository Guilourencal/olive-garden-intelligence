lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1657:1690], 1658):
    print(f'{i}: {repr(line[:100])}')
