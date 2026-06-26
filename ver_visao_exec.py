lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Visao Executiva' in line or 'visao_executiva' in line or 'radio_visao' in line:
        print(f'{i+1}: {line}', end='')
