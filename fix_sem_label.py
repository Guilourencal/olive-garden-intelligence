lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
lines[1199] = '                    fig_dow.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=30,b=10,l=10,r=10), title=dict(text=f"Semana: {sem_label}", font=dict(family="Nunito", size=10, color="#8B7A5A"), x=0), xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(showgrid=False), legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02), font=dict(family="Nunito"), height=280)'
del lines[1199-1]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('Feito!')
