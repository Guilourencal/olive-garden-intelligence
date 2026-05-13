with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'if visao_sel == "Operacao Geral":' in line:
        print(f'Inicio: {i}')
    if 'elif visao_sel == "iFood":' in line:
        print(f'Fim: {i}')
        break
