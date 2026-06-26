lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1029:1110], 1030):
    print(f'{i}: {line}', end='')
