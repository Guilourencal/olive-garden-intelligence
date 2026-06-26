lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'df_v ' in line or 'df_v=' in line or 'df_v =' in line:
        if 1320 <= i+1 <= 1360:
            print(f'{i+1}: {line}', end='')
