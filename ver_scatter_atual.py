lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[2169:2178], 2170):
    print(f'{i}: {repr(line)}')
