lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'fat_if' in line or 'df_if' in line:
        if 1040 <= i+1 <= 1120:
            print(f'{i+1}: {line}', end='')
