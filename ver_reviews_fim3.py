lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[483:492], 484):
    print(f'{i}: {repr(line[:80])}')
