lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1728:1760], 1729):
    print(f'{i}: {repr(line[:100])}')
