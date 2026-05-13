lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'fig_dow.add_trace(go.Bar(x=g_ano1' in line:
        lines[i] = lines[i].replace('textposition="outside"', 'textposition="auto"').replace('size=10, color="#8B7A5A"', 'size=9, color="white"')
        print(f'Linha {i+1} - ano anterior corrigida!')
    if 'fig_dow.add_trace(go.Bar(x=g_ult' in line:
        lines[i] = lines[i].replace('textposition="outside"', 'textposition="auto"').replace('size=10, color=MARROM', 'size=9, color="white"')
        print(f'Linha {i+1} - semana atual corrigida!')
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
