lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[480:530], 481):
    print(f'{i}: {repr(line)}')
