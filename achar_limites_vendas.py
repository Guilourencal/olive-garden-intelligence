with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'aba_sel == "Vendas"' in line:
        print(f'Inicio: {i}')
    if 'aba_sel == "OlivIA"' in line and i > 1000:
        print(f'Fim: {i}')
        break
