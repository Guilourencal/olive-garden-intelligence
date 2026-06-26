lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'OlivIA' in line and ('elif' in line or 'aba_sel' in line):
        print(f'{i+1}: {line}', end='')
