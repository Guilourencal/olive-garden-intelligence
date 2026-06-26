lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1510:1540], 1511):
    print(f'{i}: {repr(line[:90])}')
