lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1140:1160], 1141):
    print(f'{i}: {repr(line[:80])}')
