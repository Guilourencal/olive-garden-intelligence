lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'F5F0E8' in line and 'Oliv' in line and '8B9A2E' in line:
        lines[i] = '        <span style="font-family:Georgia,serif; font-size:72px; font-weight:800; letter-spacing:2px; color:#F5F0E8;">Oliv<span style="color:#8B9A2E;">ia</span></span>'
        print(f'Linha {i+1} corrigida!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
