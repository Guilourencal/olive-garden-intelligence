lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
print('=== LINHA 1030-1040 ===')
for i, line in enumerate(lines[1029:1040], 1030):
    print(f'{i}: {line}', end='')
print()
print('=== LINHA 1264-1274 ===')
for i, line in enumerate(lines[1263:1274], 1264):
    print(f'{i}: {line}', end='')
