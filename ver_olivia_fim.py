lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'elif aba_sel == "Menu"' in line or 'elif aba_sel == "Analises"' in line:
        print(f'{i+1}: {line}', end='')
