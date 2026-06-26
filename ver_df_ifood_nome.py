lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'df_ifood' in line and 'carregar' in line:
        print(f'{i+1}: {line}', end='')
