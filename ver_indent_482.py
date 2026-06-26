lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[478:488], 479):
    print(f'{i}: {repr(line)}')
