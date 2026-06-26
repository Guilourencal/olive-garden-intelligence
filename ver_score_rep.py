lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'score_externo' in line or 'pct_pos' in line or 'rep_pub' in line:
        if 1780 <= i+1 <= 1850:
            print(f'{i+1}: {line}', end='')
