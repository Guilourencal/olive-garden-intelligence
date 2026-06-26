lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'html_voz' in line or 'df_voz' in line:
        print(f'{i+1}: {line}', end='')
