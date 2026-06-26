lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'Radar de Saude' in line or 'BLOCO 1' in line:
        print(f'{i+1}: {line}', end='')
    if 'Correlacoes' in line:
        print(f'{i+1}: {line}', end='')
