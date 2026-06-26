lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'proj_total' in line and 'proj_total_ve' not in line and 'proj_if' not in line:
        if 1030 <= i+1 <= 1120:
            print(f'{i+1}: {line}', end='')
