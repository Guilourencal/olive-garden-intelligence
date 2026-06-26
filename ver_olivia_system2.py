lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1684:1700], 1685):
    print(f'{i}: {repr(line[:100])}')
