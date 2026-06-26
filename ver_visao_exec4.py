lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1109:1160], 1110):
    print(f'{i}: {line}', end='')
