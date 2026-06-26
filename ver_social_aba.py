lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'aba_sel == "Social"' in line or 'section-title' in line:
        if 617 <= i+1 <= 780:
            print(f'{i+1}: {line}', end='')
