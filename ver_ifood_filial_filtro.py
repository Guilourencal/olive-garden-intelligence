lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'df_if_ytd' in line and ('filial' in line or 'isin' in line):
        print(f'{i+1}: {line}', end='')
