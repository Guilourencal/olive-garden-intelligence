lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'Rk' in line:
        lines[i] = lines[i].replace('f"Rk"', 'f"R$ {v/1000:.0f}k"')
        print(f'Linha {i+1} corrigida!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
