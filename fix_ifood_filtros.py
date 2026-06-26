content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''            # iFood YTD — soma todos os periodos do ano atual
            df_if_ytd = df_ifood_vendas[df_ifood_vendas["periodo"].str.contains(f"/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            fat_if_ytd = df_if_ytd["faturamento"].sum() if len(df_if_ytd) > 0 else 0'''

new = '''            # iFood filtrado — mesmo periodo do salao (anos e meses selecionados)
            if len(df_ifood_vendas) > 0:
                df_if_ytd = df_ifood_vendas.copy()
                # Filtrar por ano
                df_if_ytd = df_if_ytd[df_if_ytd["periodo"].str.contains("|".join([str(a) for a in anos_sel]))]
                # Filtrar por mes se nao for todos os meses
                meses_num = {"jan":"01","fev":"02","mar":"03","abr":"04","mai":"05","jun":"06","jul":"07","ago":"08","set":"09","out":"10","nov":"11","dez":"12"}
                meses_num_sel = [meses_num[m] for m in meses_sel if m in meses_num]
                if meses_num_sel and len(meses_num_sel) < 12:
                    df_if_ytd = df_if_ytd[df_if_ytd["periodo"].str[:2].isin(meses_num_sel)]
            else:
                df_if_ytd = pd.DataFrame()
            fat_if_ytd = df_if_ytd["faturamento"].sum() if len(df_if_ytd) > 0 else 0'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
