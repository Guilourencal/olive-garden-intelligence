lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1797:1832], 1798):
    print(f'{i}: {line}', end='')
