lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[472:492], 473):
    print(f'{i}: {repr(line)}')
