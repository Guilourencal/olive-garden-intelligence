lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines[1033:1045], 1034):
    print(f'{i}: {repr(line[:80])}')
