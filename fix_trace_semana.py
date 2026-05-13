lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
# Inserir trace da semana atual apos o trace do ano anterior (linha 1198, indice 1197)
lines.insert(1198, '                    fig_dow.add_trace(go.Bar(x=g_ult["label"], y=g_ult["venda_salao"], name="Semana atual", marker_color=VERDE, text=g_ult["venda_salao"].apply(lambda v: f"R$ {v/1000:.0f}k"), textposition="auto", textfont=dict(family="Nunito", size=9, color="white")))')
# Remover update_layout duplicado (agora na linha 1201 apos insercao)
del lines[1200]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('Feito!')
