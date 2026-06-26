content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '            df_2025 = df_mensal[df_mensal["ano"]==2025].groupby(["mes_num","mes_label"])["venda_salao"].sum().reset_index().sort_values("mes_num")\n            df_2026 = df_mensal[df_mensal["ano"]==2026].groupby(["mes_num","mes_label"])["venda_salao"].sum().reset_index().sort_values("mes_num")\n            fig_mens = go.Figure()\n            fig_mens.add_trace(go.Bar(x=df_2025["mes_label"], y=df_2025["venda_salao"], name="2025", marker_color="#8B7A5A", opacity=0.7))\n            fig_mens.add_trace(go.Bar(x=df_2026["mes_label"], y=df_2026["venda_salao"], name="2026", marker_color=VERDE))'

new = '            df_2025 = df_mensal[df_mensal["ano"]==2025].groupby(["mes_num","mes_label"])["venda_salao"].sum().reset_index().sort_values("mes_num")\n            df_2026 = df_mensal[df_mensal["ano"]==2026].groupby(["mes_num","mes_label"])["venda_salao"].sum().reset_index().sort_values("mes_num")\n            df_budget = df_mensal[df_mensal["ano"]==2026].groupby(["mes_num","mes_label"])["meta_venda"].sum().reset_index().sort_values("mes_num")\n            fig_mens = go.Figure()\n            fig_mens.add_trace(go.Bar(x=df_2025["mes_label"], y=df_2025["venda_salao"], name="2025", marker_color="#8B7A5A", opacity=0.7))\n            fig_mens.add_trace(go.Bar(x=df_2026["mes_label"], y=df_2026["venda_salao"], name="2026", marker_color=VERDE))\n            fig_mens.add_trace(go.Scatter(x=df_budget["mes_label"], y=df_budget["meta_venda"], name="Budget", mode="lines+markers", line=dict(color="#B8923A", width=2, dash="dot"), marker=dict(size=8, color="#B8923A", symbol="diamond")))'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
