content = open('dashboard.py', 'r', encoding='utf-8').read()

start = content.find('\nelif aba_sel == "Menu":')
end = content.find('\nst.markdown(\n    \'<div style="text-align:center; font-size:10px; color:#B8A898;')

novo = '''
elif aba_sel == "Menu":
    st.markdown(\'<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Menu Intelligence</div>\', unsafe_allow_html=True)
    if len(df_menu) == 0:
        st.warning("Sem dados de menu. Rode importar_menu_analysis.py.")
    else:
        semanas_disp = sorted(df_menu["semana_ref"].unique(), reverse=True)
        semana_sel = semanas_disp[0]
        df_m = df_menu[df_menu["semana_ref"] == semana_sel].copy()
        df_m = df_m[~df_m["item"].str.upper().isin(["BROWNIE CORTESIA","SSB"])]
        df_m = df_m[~df_m["item"].str.upper().str.startswith("RF ")]
        df_m = df_m[df_m["type"].isin(["Star","Dog","Puzzle","Horse"])]

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            canal_sel = st.selectbox("Canal:", ["Ambos","POS","Delivery"], key="menu_canal")
        with col_f2:
            tipo_sel = st.selectbox("Tipo Boston:", ["Todos","Star","Dog","Puzzle","Horse"], key="menu_tipo")

        df_mf = df_m.copy()
        if canal_sel != "Ambos":
            df_mf = df_mf[df_mf["canal"] == canal_sel]
        if tipo_sel != "Todos":
            df_mf = df_mf[df_mf["type"] == tipo_sel]

        COR_BOSTON = {"Star": "#B8923A", "Dog": VERMELHO, "Puzzle": "#4A90D9", "Horse": VERDE}
        stars = df_mf[df_mf["type"]=="Star"]
        dogs = df_mf[df_mf["type"]=="Dog"]
        puzzles = df_mf[df_mf["type"]=="Puzzle"]
        horses = df_mf[df_mf["type"]=="Horse"]
        gross_total = df_mf["gross_sales"].sum() if df_mf["gross_sales"].sum() > 0 else 1
        df_bebs = df_mf[df_mf["item"].str.upper().str.contains("SCHW TONICA|SCHW CITRUS|FANTA GUARANA", na=False)]
        qty_bebs = df_bebs["quantity_per_check"].mean() if len(df_bebs) > 0 else 0
        uplift_medio = df_mf[df_mf["check_uplift"].notna()]["check_uplift"].mean() if df_mf["check_uplift"].notna().any() else 0

        st.markdown(f\'<div style="font-size:11px; color:#8B7A5A; margin-bottom:16px;">Referencia: {semana_sel} | {len(semanas_disp)} semana(s) de historico</div>\', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 1 — KPIs
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        with col_k1:
            with st.container(border=True):
                st.markdown(\'<div style="text-align:center;padding:8px;"><div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:4px;">GROSS SALES</div>\' + f\'<div style="font-size:24px;font-weight:500;color:#3D2B1F;">R$ {"  {:,.0f}".format(gross_total).replace(",",".")}</div>\' + f\'<div style="font-size:10px;color:#8B9A2E;">{stars["gross_sales"].sum()/gross_total*100:.0f}% Stars</div></div>\', unsafe_allow_html=True)
        with col_k2:
            with st.container(border=True):
                pct_star_mix = stars["number_of_checks"].sum()/df_mf["number_of_checks"].sum()*100 if df_mf["number_of_checks"].sum()>0 else 0
                st.markdown(\'<div style="text-align:center;padding:8px;"><div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:4px;">STARS NO MIX</div>\' + f\'<div style="font-size:24px;font-weight:500;color:#B8923A;">{len(stars)} itens</div>\' + f\'<div style="font-size:10px;color:#8B7A5A;">{pct_star_mix:.0f}% dos checks</div></div>\', unsafe_allow_html=True)
        with col_k3:
            with st.container(border=True):
                pct_puz_mix = puzzles["number_of_checks"].sum()/df_mf["number_of_checks"].sum()*100 if df_mf["number_of_checks"].sum()>0 else 0
                st.markdown(\'<div style="text-align:center;padding:8px;"><div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:4px;">PUZZLES</div>\' + f\'<div style="font-size:24px;font-weight:500;color:#4A90D9;">{len(puzzles)} itens</div>\' + f\'<div style="font-size:10px;color:#8B7A5A;">{pct_puz_mix:.0f}% dos checks</div></div>\', unsafe_allow_html=True)
        with col_k4:
            with st.container(border=True):
                cor_up = "#2e6b3e" if uplift_medio > 100 else "#B8923A"
                st.markdown(\'<div style="text-align:center;padding:8px;"><div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:4px;">CHECK UPLIFT MEDIO</div>\' + f\'<div style="font-size:24px;font-weight:500;color:{cor_up};">R$ {uplift_medio:.0f}</div>\' + \'<div style="font-size:10px;color:#8B7A5A;">valor extra por check</div></div>\', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 2 — TOP 5 POR TIPO
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Top 5 por Tipo Boston</div>\', unsafe_allow_html=True)
            col_s, col_h, col_p, col_d = st.columns(4)
            for col_t, tipo, label in [(col_s,"Star","⭐ Stars"),(col_h,"Horse","🐴 Horses"),(col_p,"Puzzle","🔵 Puzzles"),(col_d,"Dog","🔴 Dogs")]:
                df_tipo = df_mf[df_mf["type"]==tipo].sort_values("gross_sales", ascending=False).head(5)
                cor = COR_BOSTON.get(tipo, MARROM)
                with col_t:
                    st.markdown(f\'<div style="font-size:11px;font-weight:700;color:{cor};margin-bottom:8px;">{label}</div>\', unsafe_allow_html=True)
                    if len(df_tipo) == 0:
                        st.markdown(\'<div style="font-size:11px;color:#8B7A5A;">Sem itens</div>\', unsafe_allow_html=True)
                    for _, r in df_tipo.iterrows():
                        gs = "R$ {:,.0f}".format(r["gross_sales"]).replace(",",".")
                        st.markdown(
                            f\'<div style="padding:6px 0;border-bottom:1px solid #e8ddc8;">\' +
                            f\'<div style="font-size:11px;font-weight:500;color:#3D2B1F;">{r["item"][:28]}</div>\' +
                            f\'<div style="font-size:10px;color:#8B7A5A;">{gs} | {int(r["number_of_checks"])} checks</div></div>\',
                            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 3 — TABELA COMPLETA
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Todos os Itens</div>\', unsafe_allow_html=True)
            df_tab = df_mf[["item","type","canal","gross_sales","number_of_checks","ct_gross_total_check_avg","check_uplift"]].copy()
            df_tab = df_tab.sort_values("gross_sales", ascending=False)
            df_tab["gross_sales"] = df_tab["gross_sales"].apply(lambda v: "R$ {:,.0f}".format(v).replace(",",".") if pd.notna(v) else "—")
            df_tab["ct_gross_total_check_avg"] = df_tab["ct_gross_total_check_avg"].apply(lambda v: f"R$ {v:.0f}" if pd.notna(v) else "—")
            df_tab["check_uplift"] = df_tab["check_uplift"].apply(lambda v: f"R$ {v:.0f}" if pd.notna(v) else "—")
            df_tab["number_of_checks"] = df_tab["number_of_checks"].apply(lambda v: f"{int(v):,}".replace(",",".") if pd.notna(v) else "—")
            df_tab.columns = ["Item","Tipo","Canal","Gross Sales","Checks","Check Completo","Uplift"]
            st.dataframe(df_tab, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 4 — BEBIDAS PUZZLE
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Bebidas Puzzle — Script de Sugestao Ativa</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Schw Tonica + Schw Citrus + Fanta Guarana. Baseline: 1,11 un/check | Meta: 1,50 un/check.</div>\', unsafe_allow_html=True)
            baseline_beb = 1.11
            meta_beb = 1.50
            pct_g = min((qty_bebs-baseline_beb)/(meta_beb-baseline_beb)*100,100) if qty_bebs>baseline_beb else 0
            cor_g = "#2e6b3e" if qty_bebs>=meta_beb else "#B8923A" if qty_bebs>=baseline_beb else VERMELHO
            status_g = "Meta atingida!" if qty_bebs>=meta_beb else f"Faltam {meta_beb-qty_bebs:.2f} un/check para a meta"
            col_g1, col_g2 = st.columns([1,2])
            with col_g1:
                st.markdown(
                    f\'<div style="text-align:center;padding:20px;">\' +
                    f\'<div style="font-size:56px;font-weight:800;color:{cor_g};line-height:1;">{qty_bebs:.2f}</div>\' +
                    f\'<div style="font-size:11px;color:#8B7A5A;margin:6px 0;">un/check atual</div>\' +
                    f\'<div style="background:#e8ddc8;border-radius:8px;height:10px;margin:12px 0;">\' +
                    f\'<div style="background:{cor_g};width:{max(pct_g,3):.0f}%;height:10px;border-radius:8px;"></div></div>\' +
                    f\'<div style="display:flex;justify-content:space-between;font-size:10px;color:#8B7A5A;">\' +
                    f\'<span>Baseline: {baseline_beb}</span><span>Meta: {meta_beb}</span></div>\' +
                    f\'<div style="font-size:12px;font-weight:500;color:{cor_g};margin-top:8px;">{status_g}</div></div>\',
                    unsafe_allow_html=True)
            with col_g2:
                if len(df_bebs) > 0:
                    for _, r in df_bebs.iterrows():
                        cor_b = "#2e6b3e" if r["quantity_per_check"] >= meta_beb else "#B8923A" if r["quantity_per_check"] >= baseline_beb else VERMELHO
                        st.markdown(
                            f\'<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #e8ddc8;">\' +
                            f\'<div style="font-size:12px;font-weight:500;color:#3D2B1F;">{r["item"]}</div>\' +
                            f\'<div style="font-size:12px;font-weight:700;color:{cor_b};">{r["quantity_per_check"]:.2f} un/check</div>\' +
                            f\'<div style="font-size:11px;color:#8B7A5A;">{int(r["number_of_checks"])} checks</div></div>\',
                            unsafe_allow_html=True)
                else:
                    st.markdown(\'<div style="font-size:12px;color:#8B7A5A;padding:20px;">Bebidas Puzzle nao encontradas nos dados filtrados.</div>\', unsafe_allow_html=True)

'''

result = content[:start] + novo + content[end:]
open('dashboard.py', 'w', encoding='utf-8').write(result)
print(f'OK — {len(result.splitlines())} linhas')
