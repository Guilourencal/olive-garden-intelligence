lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'score_interno' in line or 'Score Interno' in line:
        if 800 <= i+1 <= 900:
            print(f'{i+1}: {line}', end='')
