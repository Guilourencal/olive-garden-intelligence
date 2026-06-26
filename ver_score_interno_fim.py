lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[890:910], 891):
    print(f'{i}: {line}', end='')
