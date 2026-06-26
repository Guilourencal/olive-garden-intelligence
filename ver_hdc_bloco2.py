lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1305:1325], 1306):
    print(f'{i}: {repr(line)}')
