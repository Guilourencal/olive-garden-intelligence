lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1796:1806], 1797):
    print(f'{i}: {repr(line)}')
