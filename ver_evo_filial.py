lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Evolucao por Filial' in line or 'cols_evo' in line or 'subplot' in line.lower():
        if 850 <= i+1 <= 1000:
            print(f'{i+1}: {line}', end='')
