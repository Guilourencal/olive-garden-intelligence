content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '            df_dias_v = df_ifood_dias[df_ifood_dias["periodo"] == periodo_sel_v].copy()\n            if len(df_dias_v) > 0:\n                ordem_dias = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]\n                df_dias_v["dia_norm"] = df_dias_v["dia_semana"].str.normalize("NFKD").str.encode("ascii","ignore").str.decode("ascii").str.strip()\n                dias_g = df_dias_v.groupby("dia_norm")["pedidos"].sum().reset_index()\n                fat_total_per = df_v[df_v["periodo"]==periodo_sel_v]["faturamento"].sum()'

new = '            # Usar periodo mais recente (mes corrente)\n            periodo_mes_atual = periodos[-1] if periodos else periodo_sel_v\n            df_dias_v = df_ifood_dias[df_ifood_dias["periodo"] == periodo_mes_atual].copy()\n            if len(df_dias_v) > 0:\n                ordem_dias = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]\n                df_dias_v["dia_norm"] = df_dias_v["dia_semana"].str.normalize("NFKD").str.encode("ascii","ignore").str.decode("ascii").str.strip()\n                dias_g = df_dias_v.groupby("dia_norm")["pedidos"].sum().reset_index()\n                fat_total_per = df_v[df_v["periodo"]==periodo_mes_atual]["faturamento"].sum()'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
