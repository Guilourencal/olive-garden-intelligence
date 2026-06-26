lines = open('aprender_modelo.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[119:140], 120):
    print(f'{i}: {line}', end='')
