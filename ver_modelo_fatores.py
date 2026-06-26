lines = open('aprender_modelo.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'p_stl' in line or 'fator_mes' in line or 'fator_dow' in line:
        print(f'{i+1}: {line}', end='')
