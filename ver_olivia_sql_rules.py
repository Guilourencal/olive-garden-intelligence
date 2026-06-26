lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1730:1740], 1731):
    print(f'{i}: {repr(line[:100])}')
