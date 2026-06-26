lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1483:1500], 1484):
    print(f'{i}: {repr(line[:90])}')
