content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '            df_2025 = df_mensal[df_mensal["ano"]==2025].groupby(["mes_num","mes_label"])["venda_salao"].sum().reset_index().sort_values("mes_num")\n            df_2026 = df_mensal[df_mensal["ano"]==2026].groupby(["mes_num","mes_label"])["venda_salao"].sum().reset_index().sort_values("mes_num")\n            fig_mens = go.Figure()\n            fig_mens.add_trace(go.Bar(x=df_2025["mes_label"], y=df_2025["venda_salao"], name="2025",\n            fig_mens.add_trace(go.Bar(x=df_2026["mes_label"], y=df_2026["venda_salao"], name="2026",'

# Mostrar trecho completo
idx = content.find('df_2025 = df_mensal')
print(repr(content[idx:idx+600]))
