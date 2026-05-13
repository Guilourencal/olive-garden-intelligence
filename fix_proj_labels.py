lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')

for i, line in enumerate(lines):
    # Corrige posicao da anotacao parcial
    if 'xref="paper", yref="paper", x=0, y=1.12' in line:
        lines[i] = '                xref="paper", yref="paper", x=0.5, y=-0.08, showarrow=False,'
        print(f'Linha {i+1} - anotacao reposicionada')
    # Corrige textposition do projetado para inside
    if 'textposition="outside"' in line and i > 1060:
        lines[i] = '                textposition="inside",'
        print(f'Linha {i+1} - textposition corrigido')
    # Corrige cor do texto projetado para branco
    if '"#8B6914"' in line and 'textfont' in line and i > 1060:
        lines[i] = '                textfont=dict(family="Nunito", size=12, color="white"),'
        print(f'Linha {i+1} - cor corrigida')

open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
