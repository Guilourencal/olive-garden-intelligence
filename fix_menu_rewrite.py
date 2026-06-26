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
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            canal_sel = st.selectbox("Canal:", ["Ambos","POS","Delivery"], key="menu_canal")
        with col_f2:
            tipo_sel = st.selectbox("Tipo Boston:", ["Todos","Star","Dog","Puzzle","Horse"], key="menu_tipo")
        with col_f3:
            st.markdown(f\'<div style="font-size:11px; color:#8B7A5A; padding-top:28px;">Referencia: {semana_sel}</div>\', unsafe_allow_html=True)
        df_mf = df_m.copy()
        if canal_sel != "Ambos":
            df_mf = df_mf[df_mf["canal"] == canal_sel]
        if tipo_sel != "Todos":
            df_mf = df_mf[df_mf["type"] == tipo_sel]
        COR_BOSTON = {"Star": "#B8923A", "Dog": VERMELHO, "Puzzle": "#4A90D9", "Horse": VERDE}
        def card_lia(leitura, insight, acao):
            return (
                \'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-top:12px;">\' +
                \'<div style="background:#e8f2eb; border-radius:8px; padding:12px;">\' +
                \'<div style="font-size:9px; font-weight:700; color:#2e6b3e; letter-spacing:2px; margin-bottom:6px;">LEITURA</div>\' +
                f\'<div style="font-size:11px; color:#3D2B1F;">{leitura}</div></div>\' +
                \'<div style="background:#f5f0e8; border-radius:8px; padding:12px;">\' +
                \'<div style="font-size:9px; font-weight:700; color:#B8923A; letter-spacing:2px; margin-bottom:6px;">INSIGHT</div>\' +
                f\'<div style="font-size:11px; color:#3D2B1F;">{insight}</div></div>\' +
                \'<div style="background:#e8f0f8; border-radius:8px; padding:12px;">\' +
                \'<div style="font-size:9px; font-weight:700; color:#4A90D9; letter-spacing:2px; margin-bottom:6px;">ACAO PROPOSTA</div>\' +
                f\'<div style="font-size:11px; color:#3D2B1F;">{acao}</div></div></div>\'
            )
        stars = df_mf[df_mf["type"]=="Star"]
        dogs = df_mf[df_mf["type"]=="Dog"]
        puzzles = df_mf[df_mf["type"]=="Puzzle"]
        horses = df_mf[df_mf["type"]=="Horse"]
        gross_total = df_mf["gross_sales"].sum()
        checks_total = int(df_mf["number_of_checks"].sum()) if df_mf["number_of_checks"].sum() > 0 else 1
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Resumo Executivo</div>\', unsafe_allow_html=True)
            col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns(5)
            with col_h1:
                st.metric("Gross Sales", f"R$ {gross_total:,.0f}".replace(",","."))
            with col_h2:
                st.metric("Stars", len(stars), delta=f"{stars['gross_sales'].sum()/gross_total*100:.0f}% do gross" if gross_total>0 else "0%")
            with col_h3:
                st.metric("Dogs", len(dogs), delta=f"{dogs['gross_sales'].sum()/gross_total*100:.0f}% do gross" if gross_total>0 else "0%")
            with col_h4:
                st.metric("Puzzles", len(puzzles), delta=f"{puzzles['gross_sales'].sum()/gross_total*100:.0f}% do gross" if gross_total>0 else "0%")
            with col_h5:
                st.metric("Horses", len(horses), delta=f"{horses['gross_sales'].sum()/gross_total*100:.0f}% do gross" if gross_total>0 else "0%")
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T1 — Saude da Demanda</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Quem esta gerando volume de pedidos — deteccao precoce de mudancas de demanda.</div>\', unsafe_allow_html=True)
            df_t1 = df_mf.sort_values("number_of_checks", ascending=False).head(20)
            fig_t1 = go.Figure(go.Bar(
                x=df_t1["item"].str[:28], y=df_t1["number_of_checks"],
                marker_color=[COR_BOSTON.get(t, MARROM) for t in df_t1["type"]],
                text=df_t1["number_of_checks"], textposition="outside",
                textfont=dict(family="Nunito", size=9, color=MARROM)))
            fig_t1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=90,l=10,r=10),
                xaxis=dict(tickangle=-40, tickfont=dict(family="Nunito", size=9, color=MARROM)),
                yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=340)
            st.plotly_chart(fig_t1, use_container_width=True, key="fig_t1_menu")
            checks_star = int(stars["number_of_checks"].sum()) if len(stars)>0 else 0
            checks_dog = int(dogs["number_of_checks"].sum()) if len(dogs)>0 else 0
            st.markdown(card_lia(
                leitura=f"Stars concentram {checks_star:,} checks ({checks_star/checks_total*100:.0f}% do total). Dogs ainda movem {checks_dog:,} checks ({checks_dog/checks_total*100:.0f}%) — nao sao ignorados pelo cliente.",
                insight="Alto volume de checks em Dogs indica que o problema nao e demanda — e posicionamento e margem. O cliente quer esses itens.",
                acao="Auditar precificacao e custo dos Dogs com maior volume. Avaliar se cabem em promocoes de mix para puxar Stars junto."
            ), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T2 — Qualidade de Receita</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Revenue Score e Check Uplift revelam o impacto real — alem do Gross Sales isolado.</div>\', unsafe_allow_html=True)
            dog_check_avg = dogs["ct_gross_total_check_avg"].mean() if len(dogs)>0 else 0
            star_check_avg = stars["ct_gross_total_check_avg"].mean() if len(stars)>0 else 0
            if pd.notna(dog_check_avg) and dog_check_avg>0:
                st.markdown(
                    f\'<div style="background:#3D2B1F; border-radius:8px; padding:12px 16px; margin-bottom:16px; border-left:4px solid #B8923A;">\' +
                    f\'<span style="font-size:12px; color:#F5F0E8;">💡 <b>Insight critico:</b> Dogs tem check completo medio <b style="color:#B8923A;">R$ {dog_check_avg:.0f}</b> — maior que Stars (<b>R$ {star_check_avg:.0f}</b>). Quando o cliente pede um Dog, a mesa gasta mais. O problema e visibilidade, nao o cliente.</span></div>\',
                    unsafe_allow_html=True)
            col_t2a, col_t2b = st.columns(2)
            with col_t2a:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Revenue Score vs Gross Sales por Tipo</div>\', unsafe_allow_html=True)
                df_t2 = df_mf.groupby("type").agg(revenue_score=("revenue_score","sum"), gross_sales=("gross_sales","sum")).reset_index()
                fig_t2 = go.Figure()
                fig_t2.add_trace(go.Bar(x=df_t2["type"], y=df_t2["gross_sales"], name="Gross Sales", marker_color="#8B7A5A", opacity=0.7))
                fig_t2.add_trace(go.Bar(x=df_t2["type"], y=df_t2["revenue_score"], name="Revenue Score", marker_color=VERDE))
                fig_t2.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False),
                    legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                    font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_t2, use_container_width=True, key="fig_t2a_menu")
            with col_t2b:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Top 10 Check Uplift — Poder de Basket</div>\', unsafe_allow_html=True)
                df_uplift = df_mf[df_mf["check_uplift"].notna()].sort_values("check_uplift", ascending=False).head(10)
                fig_uplift = go.Figure(go.Bar(
                    y=df_uplift["item"].str[:25], x=df_uplift["check_uplift"], orientation="h",
                    marker_color=[COR_BOSTON.get(t, MARROM) for t in df_uplift["type"]],
                    text=df_uplift["check_uplift"].apply(lambda v: f"R$ {v:.0f}"),
                    textposition="outside", textfont=dict(family="Nunito", size=9, color=MARROM)))
                fig_uplift.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=50),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(tickfont=dict(family="Nunito", size=9, color=MARROM)),
                    font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_uplift, use_container_width=True, key="fig_t2b_menu")
            top_uplift = df_mf[df_mf["check_uplift"].notna()].sort_values("check_uplift", ascending=False)
            if len(top_uplift)>0:
                ti = top_uplift.iloc[0]
                st.markdown(card_lia(
                    leitura=f"Dogs geram check completo medio R$ {dog_check_avg:.0f} vs Stars R$ {star_check_avg:.0f}. Maior Check Uplift: {ti['item']} (R$ {ti['check_uplift']:.0f} acima da media quando presente).",
                    insight="Revenue Score revela itens subvalorizados pelo Gross Sales isolado — um item com pouco gross pode estar gerando muito valor ao puxar outros itens na mesa.",
                    acao="Priorizar itens com alto Check Uplift nos scripts de sugestao ativa. Revisar posicionamento de Dogs com check completo acima de R$ 280."
                ), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T3 — Pressao de Desconto</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Dependencia promocional por item — risco de erosao de receita.</div>\', unsafe_allow_html=True)
            df_t3 = df_mf[df_mf["discounts"].notna() & (df_mf["gross_sales"]>0)].copy()
            df_t3["pct_desc"] = df_t3["discounts"] / df_t3["gross_sales"] * 100
            alertas = df_t3[df_t3["pct_desc"]>5]
            if len(alertas)>0:
                nomes = ", ".join(alertas["item"].str[:20].tolist())
                st.markdown(f\'<div style="background:#f5e8e8; border-radius:8px; padding:10px 14px; margin-bottom:12px; border-left:4px solid {VERMELHO};"><span style="font-size:12px; color:#8B2E2E;">⚠️ {len(alertas)} item(ns) com desconto acima de 5% do Gross: {nomes}</span></div>\', unsafe_allow_html=True)
            df_t3_top = df_t3.sort_values("discounts", ascending=False).head(10)
            fig_t3 = go.Figure(go.Bar(
                x=df_t3_top["item"].str[:25], y=df_t3_top["discounts"],
                marker_color=[COR_BOSTON.get(t, MARROM) for t in df_t3_top["type"]],
                text=df_t3_top.apply(lambda r: f"R$ {r['discounts']:,.0f} ({r['pct_desc']:.1f}%)".replace(",","."), axis=1),
                textposition="outside", textfont=dict(family="Nunito", size=9, color=MARROM)))
            fig_t3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=90,l=10,r=10),
                xaxis=dict(tickangle=-40, tickfont=dict(family="Nunito", size=9, color=MARROM)),
                yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=320)
            st.plotly_chart(fig_t3, use_container_width=True, key="fig_t3_menu")
            desc_stars = df_t3[df_t3["type"]=="Star"]["pct_desc"].mean()
            desc_dogs = df_t3[df_t3["type"]=="Dog"]["pct_desc"].mean()
            st.markdown(card_lia(
                leitura=f"Stars tem desconto medio de {desc_stars:.1f}% do gross — saudavel. Dogs em {desc_dogs:.1f}%. {len(alertas)} item(ns) com desconto acima de 5%.",
                insight="Desconto alto em Dogs pode indicar uso de promocao para compensar baixa visibilidade — subsidio involuntario que nao resolve o problema estrutural.",
                acao="Mapear Dogs com desconto alto e potencial de reposicionamento. Reduzir desconto gradualmente e monitorar impacto em checks por 2 semanas."
            ), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T4 — Basket e Mix</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Mix Boston e eficacia do script de sugestao ativa de bebidas Puzzle.</div>\', unsafe_allow_html=True)
            col_t4a, col_t4b = st.columns(2)
            with col_t4a:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Mix Boston — Distribuicao de Checks</div>\', unsafe_allow_html=True)
                mix = df_mf.groupby("type")["number_of_checks"].sum().reset_index()
                mix["pct"] = mix["number_of_checks"] / mix["number_of_checks"].sum() * 100
                fig_mix = go.Figure(go.Pie(
                    labels=mix["type"], values=mix["pct"].round(1),
                    marker_colors=[COR_BOSTON.get(t, MARROM) for t in mix["type"]],
                    textfont=dict(family="Nunito", size=12), hole=0.4))
                fig_mix.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10),
                    font=dict(family="Nunito"), height=240,
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM)))
                st.plotly_chart(fig_mix, use_container_width=True, key="fig_t4a_menu")
            with col_t4b:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Bebidas Puzzle — Qty/Check vs Meta</div>\', unsafe_allow_html=True)
                df_bebs = df_mf[df_mf["item"].str.upper().str.contains("SCHW TONICA|SCHW CITRUS|FANTA GUARANA", na=False)]
                qty_atual = df_bebs["quantity_per_check"].mean() if len(df_bebs)>0 else 0
                baseline_beb = 1.11
                meta_beb = 1.50
                pct_g = min((qty_atual-baseline_beb)/(meta_beb-baseline_beb)*100,100) if qty_atual>baseline_beb else 0
                cor_g = "#2e6b3e" if qty_atual>=meta_beb else "#B8923A" if qty_atual>=baseline_beb else VERMELHO
                status_g = "Meta atingida!" if qty_atual>=meta_beb else f"Faltam {meta_beb-qty_atual:.2f} un/check para a meta"
                st.markdown(
                    f\'<div style="text-align:center; padding:16px;">\' +
                    f\'<div style="font-size:11px; color:#8B7A5A; margin-bottom:4px;">Schw Tonica + Schw Citrus + Fanta Guarana</div>\' +
                    f\'<div style="font-size:52px; font-weight:800; color:{cor_g}; line-height:1;">{qty_atual:.2f}</div>\' +
                    f\'<div style="font-size:11px; color:#8B7A5A; margin:4px 0;">un/check atual</div>\' +
                    f\'<div style="background:#e8ddc8; border-radius:8px; height:10px; margin:12px 0;">\' +
                    f\'<div style="background:{cor_g}; width:{max(pct_g,3):.0f}%; height:10px; border-radius:8px;"></div></div>\' +
                    f\'<div style="display:flex; justify-content:space-between; font-size:10px; color:#8B7A5A;">\' +
                    f\'<span>Baseline: {baseline_beb}</span><span>Meta: {meta_beb}</span></div>\' +
                    f\'<div style="font-size:11px; color:{cor_g}; margin-top:8px; font-weight:700;">{status_g}</div></div>\',
                    unsafe_allow_html=True)
            pct_star_c = stars["number_of_checks"].sum()/checks_total*100 if checks_total>0 else 0
            pct_puz_c = puzzles["number_of_checks"].sum()/checks_total*100 if checks_total>0 else 0
            st.markdown(card_lia(
                leitura=f"Stars representam {pct_star_c:.0f}% dos checks. Puzzles estao em {pct_puz_c:.0f}% — potencial nao explorado. Bebidas Puzzle em {qty_atual:.2f} un/check (baseline {baseline_beb}, meta {meta_beb}).",
                insight="Puzzles tem alta margem e baixa demanda — o cliente compra quando recomendado. O gap entre baseline e meta indica que o script de sugestao ainda nao esta sistematico.",
                acao="Treinar garcons no script de sugestao ativa para bebidas Puzzle. Meta de 1,50 representa +35% vs baseline — monitorar evolucao semanal apos implementacao."
            ), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T5 — POS vs Delivery</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Dois canais com logicas distintas — estrategias e oportunidades separadas.</div>\', unsafe_allow_html=True)
            col_pos, col_dlv = st.columns(2)
            for col_c, canal_t5 in [(col_pos,"POS"),(col_dlv,"Delivery")]:
                df_canal = df_m[df_m["canal"]==canal_t5]
                df_canal = df_canal[df_canal["type"].isin(["Star","Dog","Puzzle","Horse"])]
                gross_c = df_canal["gross_sales"].sum()
                rev_c = df_canal["revenue_score"].sum()
                check_c = df_canal["ct_gross_total_check_avg"].mean()
                guest_c = df_canal["ct_guest_average"].mean()
                top5 = df_canal.sort_values("revenue_score", ascending=False).head(5)
                with col_c:
                    st.markdown(f\'<div style="font-size:14px; font-weight:800; color:#3D2B1F; margin-bottom:12px; text-align:center; border-bottom:2px solid #8B9A2E; padding-bottom:8px;">{canal_t5}</div>\', unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("Gross Sales", f"R$ {gross_c:,.0f}".replace(",","."))
                        st.metric("Check Medio", f"R$ {check_c:.0f}" if pd.notna(check_c) else "—")
                    with c2:
                        st.metric("Revenue Score", f"R$ {rev_c:,.0f}".replace(",","."))
                        st.metric("Guest Average", f"R$ {guest_c:.0f}" if pd.notna(guest_c) else "—")
                    st.markdown(\'<div style="font-size:10px; color:#8B7A5A; margin:8px 0 4px 0; font-weight:700;">TOP 5 POR REVENUE SCORE</div>\', unsafe_allow_html=True)
                    for _, r in top5.iterrows():
                        cor = COR_BOSTON.get(r["type"], MARROM)
                        st.markdown(
                            f\'<div style="display:flex; justify-content:space-between; align-items:center; padding:5px 0; border-bottom:1px solid #e8ddc8;">\' +
                            f\'<span style="font-size:10px; color:#3D2B1F;">{r["item"][:24]}</span>\' +
                            f\'<span style="font-size:9px; font-weight:700; color:{cor}; background:{cor}22; padding:2px 6px; border-radius:4px;">{r["type"]}</span></div>\',
                            unsafe_allow_html=True)
                    if canal_t5=="Delivery":
                        puzz_dlv = df_canal[df_canal["type"]=="Puzzle"]["ct_guest_average"].mean()
                        if pd.notna(puzz_dlv) and puzz_dlv>0:
                            st.markdown(
                                f\'<div style="background:#1a1209; border-radius:8px; padding:12px; margin-top:12px; border:1px solid #8B9A2E; text-align:center;">\' +
                                f\'<div style="font-size:9px; color:#8B9A2E; letter-spacing:2px; margin-bottom:4px;">GUEST AVG PUZZLES DELIVERY</div>\' +
                                f\'<div style="font-size:36px; font-weight:800; color:#8B9A2E;">R$ {puzz_dlv:.0f}</div>\' +
                                f\'<div style="font-size:9px; color:#8B7A5A; margin-top:4px;">maior guest average do portfolio delivery</div></div>\',
                                unsafe_allow_html=True)
            gross_pos = df_m[df_m["canal"]=="POS"]["gross_sales"].sum()
            gross_dlv = df_m[df_m["canal"]=="Delivery"]["gross_sales"].sum()
            pct_dlv = gross_dlv/(gross_pos+gross_dlv)*100 if (gross_pos+gross_dlv)>0 else 0
            guest_pos_m = df_m[df_m["canal"]=="POS"]["ct_guest_average"].mean()
            guest_dlv_m = df_m[df_m["canal"]=="Delivery"]["ct_guest_average"].mean()
            st.markdown(card_lia(
                leitura=f"Delivery representa {pct_dlv:.1f}% do Gross Sales mas tem Guest Average de R$ {guest_dlv_m:.0f} vs R$ {guest_pos_m:.0f} no POS. Puzzles delivery tem o maior guest average do portfolio.",
                insight="O canal Delivery e menor em volume mas mais eficiente por cliente. Puzzles delivery sao especialmente valiosos — cliente que pede Puzzle no delivery gasta mais por pessoa.",
                acao="Criar bundle exclusivo de Puzzles para Delivery. Avaliar visibilidade dos Puzzles no iFood — posicionamento nas primeiras posicoes do cardapio digital."
            ), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T6 — Tempo: Dia e Turno</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Concentracao de receita por slot temporal — onde estao as oportunidades subutilizadas.</div>\', unsafe_allow_html=True)
            col_t6a, col_t6b = st.columns(2)
            with col_t6a:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Gross Sales por Dia mais Popular</div>\', unsafe_allow_html=True)
                df_dia = df_mf.copy()
                df_dia["dia"] = df_dia["most_popular_day"].str.split(" ").str[0]
                dias_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
                dias_label = {"Monday":"Seg","Tuesday":"Ter","Wednesday":"Qua","Thursday":"Qui","Friday":"Sex","Saturday":"Sab","Sunday":"Dom"}
                dia_gross = df_dia.groupby("dia")["gross_sales"].sum().reindex(dias_order).reset_index()
                dia_gross.columns = ["dia","gross"]
                dia_gross["label"] = dia_gross["dia"].map(dias_label)
                dia_gross["gross"] = dia_gross["gross"].fillna(0)
                fig_dia = go.Figure(go.Bar(
                    x=dia_gross["label"], y=dia_gross["gross"],
                    marker_color=["#B8923A" if d in ["Saturday","Sunday"] else "#8B7A5A" for d in dia_gross["dia"]],
                    text=dia_gross["gross"].apply(lambda v: f"R$ {v/1000:.0f}k" if v>0 else ""),
                    textposition="outside", textfont=dict(family="Nunito", size=10, color=MARROM)))
                fig_dia.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=250)
                st.plotly_chart(fig_dia, use_container_width=True, key="fig_t6a_menu")
            with col_t6b:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Gross Sales por Turno</div>\', unsafe_allow_html=True)
                df_turno = df_mf.copy()
                df_turno["turno"] = df_turno["most_popular_day_part"].str.split(" ").str[0]
                turno_gross = df_turno.groupby("turno")["gross_sales"].sum().reset_index()
                turno_total = turno_gross["gross_sales"].sum()
                turno_gross["pct"] = turno_gross["gross_sales"]/turno_total*100
                fig_turno = go.Figure(go.Pie(
                    labels=turno_gross["turno"], values=turno_gross["gross_sales"].round(0),
                    marker_colors=[VERDE,"#B8923A","#8B7A5A"][:len(turno_gross)],
                    textfont=dict(family="Nunito", size=12), hole=0.4,
                    texttemplate="%{label}<br>%{percent}"))
                fig_turno.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    font=dict(family="Nunito"), height=250,
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM)))
                st.plotly_chart(fig_turno, use_container_width=True, key="fig_t6b_menu")
            pct_fds = dia_gross[dia_gross["dia"].isin(["Saturday","Sunday"])]["gross"].sum()/dia_gross["gross"].sum()*100 if dia_gross["gross"].sum()>0 else 0
            almoco_rows = turno_gross[turno_gross["turno"]=="Lunch"]["pct"]
            almoco_pct = almoco_rows.values[0] if len(almoco_rows)>0 else 0
            st.markdown(card_lia(
                leitura=f"Sabado e Domingo concentram {pct_fds:.0f}% do Gross Sales. Almoco representa {almoco_pct:.0f}% do gross — jantar e o turno com maior espaco de crescimento.",
                insight="Concentracao no fds/almoco cria risco operacional — qualquer problema nesses slots tem impacto desproporcionalmente alto. Jantar e o turno subutilizado com maior potencial de Puzzles.",
                acao="Criar acao especifica de Puzzles para jantar de semana — turno com menos pressao operacional e mais tempo para sugestao ativa. Avaliar experiencias para atrair jantar."
            ), unsafe_allow_html=True)

'''

result = content[:start] + novo + content[end:]
open('dashboard.py', 'w', encoding='utf-8').write(result)
print(f'OK — {len(result.splitlines())} linhas')
