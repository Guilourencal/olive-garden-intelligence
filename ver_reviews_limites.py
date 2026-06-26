lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'aba_sel == "Reviews"' in line or ('elif aba_sel ==' in line and i > 200):
        print(f'{i+1}: {line}', end='')
