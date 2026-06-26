content = open('dashboard.py', 'r', encoding='utf-8').read()

old = "            st.markdown('<div class=\"section-title\">Visao Executiva — Salao</div>', unsafe_allow_html=True)\n            cols_c = st.columns(4)"
new = """            st.markdown('<div class=\"section-title\">Visao Executiva — Salao + iFood</div>', unsafe_allow_html=True)
            # iFood MTD
            from datetime import date as _date_ve
            _hoje_ve = _date_ve.today()
            _periodo_if = f"01/{_hoje_ve.month:02d}/{_hoje_ve.year} - {_hoje_ve.day:02d}/{_hoje_ve.month:02d}/{_hoje_ve.year}"
            df_if_mtd = df_ifood_vendas[df_ifood_vendas["periodo"].str.startswith(f"01/{_hoje_ve.month:02d}/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            if len(df_if_mtd) == 0:
                df_if_mtd = df_ifood_vendas[df_ifood_vendas["periodo"].str.contains(f"/{_hoje_ve.month:02d}/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            fat_if_mtd = df_if_mtd["faturamento"].sum() if len(df_if_mtd) > 0 else 0
            cols_c = st.columns(6)"""

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK step 1')
else:
    print('TRECHO NAO ENCONTRADO step 1')
