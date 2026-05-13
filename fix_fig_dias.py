lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
# Inserir a criacao do fig_dias antes do update_layout
for i, line in enumerate(lines):
    if 'fig_dias.update_layout' in line and 'height=380' in line:
        lines.insert(i, '                fig_dias = go.Figure(go.Bar(x=df_dias_g["dia_norm"], y=df_dias_g["pedidos"], marker_color=VERDE, text=df_dias_g["pedidos"], textposition="outside", textfont=dict(family="Nunito", size=12, color=MARROM)))')
        print(f'Linha {i+1} - fig_dias inserido!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
