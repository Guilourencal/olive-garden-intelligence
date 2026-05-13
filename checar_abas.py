with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'elif aba_sel' in line:
        print(f'{i}: {line}', end='')
