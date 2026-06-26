lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'df_mes_hdc' in line or '_hoje' in line:
        if 1300 <= i+1 <= 1340:
            print(f'{i+1}: {line}', end='')
