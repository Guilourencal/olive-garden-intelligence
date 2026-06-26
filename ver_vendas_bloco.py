lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[992:1045], 993):
    print(f'{i}: {line}', end='')
