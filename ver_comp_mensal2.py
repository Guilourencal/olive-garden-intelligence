lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1286:1330], 1287):
    print(f'{i}: {repr(line[:100])}')
