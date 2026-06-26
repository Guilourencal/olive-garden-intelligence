content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '                    salao_p = venda_salao_mes[venda_salao_mes["mes_ano"] == mes_ano_key]["'
new = '                    # Apenas filiais com iFood\n                    filiais_com_ifood = ["Olive Garden - Morumbi","Olive Garden - Center Norte","Olive Garden - Aricanduva","Olive Garden - Dom Pedro"]\n                    venda_salao_ifood = df_vd_share[df_vd_share["filial"].isin(filiais_com_ifood)].groupby("mes_ano")["venda_salao"].sum().reset_index()\n                    venda_salao_ifood.columns = ["mes_ano","salao"]\n                    salao_p = venda_salao_ifood[venda_salao_ifood["mes_ano"] == mes_ano_key]["'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
