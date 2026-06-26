lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[925:945], 926):
    print(f'{i}: {line}', end='')
