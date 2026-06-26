lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'ranking["indice"]' in line and 'astype(int)' in line:
        lines[i] = lines[i].replace('.astype(int)', '.fillna(0).astype(int)')
        print(f'Corrigido linha {i+1}')
        break
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
