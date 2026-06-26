lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[809:835], 810):
    print(f'{i}: {line}', end='')
