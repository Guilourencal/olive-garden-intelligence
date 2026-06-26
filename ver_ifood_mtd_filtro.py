lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'fat_if_mtd' in line or 'df_if_mtd' in line:
        if 1030 <= i+1 <= 1060:
            print(f'{i+1}: {line}', end='')
