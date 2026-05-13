with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'Reviews Recentes' in line or 'reviews_recentes' in line.lower() or 'tabela' in line.lower() and 'download' in line.lower():
        print(f'{i}: {line}', end='')
    if 'elif aba_sel == "Social"' in line:
        print(f'{i}: {line}', end='')
