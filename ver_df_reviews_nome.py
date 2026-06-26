lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'carregar_reviews' in line or 'df_reviews' in line:
        if 220 <= i+1 <= 240:
            print(f'{i+1}: {line}', end='')
