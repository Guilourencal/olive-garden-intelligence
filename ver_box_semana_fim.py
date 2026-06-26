lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1244:1295], 1245):
    print(f'{i}: {line}', end='')
