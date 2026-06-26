lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'df_comments' in line and 'def ' not in line:
        if 780 <= i+1 <= 830:
            print(f'{i+1}: {line}', end='')
