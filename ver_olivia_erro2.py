lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1803:1815], 1804):
    print(f'{i}: {repr(line)}')
