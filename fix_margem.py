lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'r=200' in line and 'margin' in line:
        lines[i] = lines[i].replace('r=200', 'r=250')
        print(f'Linha {i+1} corrigida - margem aumentada para 250')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
