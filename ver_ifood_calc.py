lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'fat_if_ytd' in line or 'df_if_ytd' in line or 'fat_if_mtd' in line or 'df_if_mtd' in line:
        print(f'{i+1}: {line}', end='')
