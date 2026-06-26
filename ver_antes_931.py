lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[825:835], 826):
    print(f'{i}: {line}', end='')
