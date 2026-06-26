lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[894:960], 895):
    print(f'{i}: {line}', end='')
