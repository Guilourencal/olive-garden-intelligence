with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1094:1104], 1095):
    print(f'{i}: {repr(line)}')
