lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'elif aba_sel == "Vendas"' in line:
        print(f'{i+1}: {line}', end='')
    if 'vt_fmt' in line:
        print(f'{i+1}: {line}', end='')
        break
