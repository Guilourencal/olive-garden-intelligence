lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'df_comments_f' in line and ('copy' in line or '=' in line):
        if 790 <= i+1 <= 830:
            print(f'{i+1}: {line}', end='')
