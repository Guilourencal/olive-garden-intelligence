content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''            df_if_mtd = df_ifood_vendas[df_ifood_vendas["periodo"].str.startswith(f"01/{_hoje_ve.month:02d}/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            if len(df_if_mtd) == 0:
                df_if_mtd = df_ifood_vendas[df_ifood_vendas["periodo"].str.contains(f"/{_hoje_ve.month:02d}/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            fat_if_mtd = df_if_mtd["faturamento"].sum() if len(df_if_mtd) > 0 else 0'''

new = '''            df_if_mtd = df_ifood_vendas[df_ifood_vendas["periodo"].str.startswith(f"01/{_hoje_ve.month:02d}/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            if len(df_if_mtd) == 0:
                df_if_mtd = df_ifood_vendas[df_ifood_vendas["periodo"].str.contains(f"/{_hoje_ve.month:02d}/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            fat_if_mtd = df_if_mtd["faturamento"].sum() if len(df_if_mtd) > 0 else 0
            # iFood YTD — soma todos os periodos do ano atual
            df_if_ytd = df_ifood_vendas[df_ifood_vendas["periodo"].str.contains(f"/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            fat_if_ytd = df_if_ytd["faturamento"].sum() if len(df_if_ytd) > 0 else 0'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
