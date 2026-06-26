lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1068:1090], 1069):
    print(f'{i}: {repr(line[:100])}')
