lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1155:1175], 1156):
    print(f'{i}: {repr(line[:80])}')
