content = open('dashboard.py', 'r', encoding='utf-8').read()

menu_block = '''
elif aba_sel == "Menu":
    st.markdown('<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Menu Intelligence</div>', unsafe_allow_html=True)

    if len(df_menu) == 0:
        st.warning("Sem dados de menu disponíveis. Rode importar_menu_analysis.py.")
    else:
        # Filtros e configuracao
        semanas_disp = sorted(df_menu["semana_ref"].unique(), reverse=True)
        semana_sel = semanas_disp[0]
        ultima_atualizacao = str(semana_sel)
        df_m = df_menu[df_menu["semana_ref"] == semana_sel].copy()

        # Excluir itens operacionais
        excluir = ["BROWNIE CORTESIA", "SSB"]
        df_m = df_m[~df_m["item"].str.upper().isin(excluir)]
        df_m = df_m[~df_m["item"].str.upper().str.startswith("RF ")]
        df_m = df_m[df_m["type"].isin(["Star","Dog","Puzzle","Horse"])]

        # Filtros globais
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            canal_sel = st.selectbox("Canal:", ["Ambos","POS","Delivery"], key="menu_canal")
        with col_f2:
            tipos_disp = ["Todos"] + sorted(df_m["type"].dropna().unique().tolist())
            tipo_sel = st.selectbox("Tipo Boston:", tipos_disp, key="menu_tipo")
        with col_f3:
            st.markdown(f\'<div style="font-size:11px; color:#8B7A5A; padding-top:28px;">Referencia: {ultima_atualizacao}</div>\', unsafe_allow_html=True)

        df_mf = df_m.copy()
        if canal_sel != "Ambos":
            df_mf = df_mf[df_mf["canal"] == canal_sel]
        if tipo_sel != "Todos":
            df_mf = df_mf[df_mf["type"] == tipo_sel]

        COR_BOSTON = {"Star": "#B8923A", "Dog": VERMELHO, "Puzzle": "#4A90D9", "Horse": VERDE}

        st.markdown("<br>", unsafe_allow_html=True)

        # RESUMO EXECUTIVO
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Resumo Executivo</div>\', unsafe_allow_html=True)
            col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns(5)
            total_items = len(df_mf)
            gross_total = df_mf["gross_sales"].sum()
            stars = df_mf[df_mf["type"]=="Star"]
            dogs = df_mf[df_mf["type"]=="Dog"]
            puzzles = df_mf[df_mf["type"]=="Puzzle"]
            horses = df_mf[df_mf["type"]=="Horse"]
            with col_h1:
                st.metric("Total Itens", total_items)
            with col_h2:
                st.metric("Gross Sales", f"R$ {gross_total:,.0f}".replace(",","."))
            with col_h3:
                st.metric("Stars", len(stars), delta=f"{len(stars)/total_items*100:.0f}% do mix")
            with col_h4:
                st.metric("Puzzles", len(puzzles), delta=f"{len(puzzles)/total_items*100:.0f}% do mix")
            with col_h5:
                st.metric("Dogs", len(dogs), delta=f"{len(dogs)/total_items*100:.0f}% do mix")

        st.markdown("<br>", unsafe_allow_html=True)

        # TIER 1 — SAUDE DA DEMANDA
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T1 — Saude da Demanda</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Top itens por volume de checks — detecta quem move a demanda.</div>\', unsafe_allow_html=True)
            df_t1 = df_mf.sort_values("number_of_checks", ascending=False).head(20)
            fig_t1 = go.Figure(go.Bar(
                x=df_t1["item"].str[:30],
                y=df_t1["number_of_checks"],
                marker_color=[COR_BOSTON.get(t, MARROM) for t in df_t1["type"]],
                text=df_t1["number_of_checks"],
                textposition="outside",
                textfont=dict(family="Nunito", size=9, color=MARROM)
            ))
            fig_t1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=80,l=10,r=10),
                xaxis=dict(tickangle=-35, tickfont=dict(family="Nunito", size=9, color=MARROM)),
                yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=320)
            st.plotly_chart(fig_t1, use_container_width=True, key="fig_t1_menu")

        st.markdown("<br>", unsafe_allow_html=True)

        # TIER 2 — QUALIDADE DE RECEITA
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T2 — Qualidade de Receita</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Revenue Score revela o impacto real de cada item — vai alem do Gross Sales isolado.</div>\', unsafe_allow_html=True)

            # Insight Dogs
            dog_check_avg = dogs["ct_gross_total_check_avg"].mean()
            star_check_avg = stars["ct_gross_total_check_avg"].mean()
            if pd.notna(dog_check_avg) and pd.notna(star_check_avg):
                st.markdown(
                    f\'<div style="background:#3D2B1F; border-radius:8px; padding:12px 16px; margin-bottom:16px; border-left:4px solid #B8923A;">\'\
                    f\'<span style="font-size:12px; color:#F5F0E8;">💡 <b>Insight:</b> Dogs tem check completo medio \'\
                    f\'<b style="color:#B8923A;">R$ {dog_check_avg:.0f}</b> — maior que Stars \'\
                    f\'(<b>R$ {star_check_avg:.0f}</b>). O problema e visibilidade, nao o cliente.</span></div>\',
                    unsafe_allow_html=True
                )

            col_t2a, col_t2b = st.columns(2)
            with col_t2a:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Revenue Score por Tipo Boston</div>\', unsafe_allow_html=True)
                df_t2 = df_mf.groupby("type").agg(revenue_score=("revenue_score","sum"), gross_sales=("gross_sales","sum")).reset_index()
                fig_t2 = go.Figure()
                fig_t2.add_trace(go.Bar(x=df_t2["type"], y=df_t2["gross_sales"], name="Gross Sales", marker_color="#8B7A5A", opacity=0.7))
                fig_t2.add_trace(go.Bar(x=df_t2["type"], y=df_t2["revenue_score"], name="Revenue Score", marker_color=VERDE))
                fig_t2.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False), legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                    font=dict(family="Nunito"), height=280)
                st.plotly_chart(fig_t2, use_container_width=True, key="fig_t2a_menu")
            with col_t2b:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Top 10 Check Uplift (poder de basket)</div>\', unsafe_allow_html=True)
                df_uplift = df_mf[df_mf["check_uplift"].notna()].sort_values("check_uplift", ascending=False).head(10)
                fig_uplift = go.Figure(go.Bar(
                    y=df_uplift["item"].str[:25],
                    x=df_uplift["check_uplift"],
                    orientation="h",
                    marker_color=[COR_BOSTON.get(t, MARROM) for t in df_uplift["type"]],
                    text=df_uplift["check_uplift"].apply(lambda v: f"R$ {v:.0f}"),
                    textposition="outside",
                    textfont=dict(family="Nunito", size=9, color=MARROM)
                ))
                fig_uplift.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=40),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(tickfont=dict(family="Nunito", size=9, color=MARROM)),
                    font=dict(family="Nunito"), height=280)
                st.plotly_chart(fig_uplift, use_container_width=True, key="fig_t2b_menu")

        st.markdown("<br>", unsafe_allow_html=True)

        # TIER 3 — PRESSAO DE DESCONTO
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T3 — Pressao de Desconto</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Dependencia promocional e risco de erosao de receita.</div>\', unsafe_allow_html=True)
            df_t3 = df_mf[df_mf["discounts"].notna() & (df_mf["discounts"] > 0)].copy()
            df_t3["pct_desconto"] = df_t3["discounts"] / df_t3["gross_sales"] * 100
            df_t3_alerta = df_t3[df_t3["pct_desconto"] > 5].sort_values("discounts", ascending=False).head(10)
            if len(df_t3_alerta) > 0:
                st.markdown(f\'<div style="background:#f5e8e8; border-radius:8px; padding:10px; margin-bottom:12px; border-left:4px solid #B8923A;"><span style="font-size:12px; color:#8B2E2E;">⚠️ {len(df_t3_alerta)} itens com desconto acima de 5% do Gross Sales</span></div>\', unsafe_allow_html=True)
            df_t3_top = df_mf[df_mf["discounts"].notna()].sort_values("discounts", ascending=False).head(10)
            fig_t3 = go.Figure(go.Bar(
                x=df_t3_top["item"].str[:25],
                y=df_t3_top["discounts"],
                marker_color=[COR_BOSTON.get(t, MARROM) for t in df_t3_top["type"]],
                text=df_t3_top["discounts"].apply(lambda v: f"R$ {v:,.0f}".replace(",",".")),
                textposition="outside",
                textfont=dict(family="Nunito", size=9, color=MARROM)
            ))
            fig_t3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=80,l=10,r=10),
                xaxis=dict(tickangle=-35, tickfont=dict(family="Nunito", size=9, color=MARROM)),
                yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=300)
            st.plotly_chart(fig_t3, use_container_width=True, key="fig_t3_menu")

        st.markdown("<br>", unsafe_allow_html=True)

        # TIER 4 — BASKET & MIX
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T4 — Basket & Mix</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Mix Boston e bebidas Puzzle — eficacia do script de sugestao ativa.</div>\', unsafe_allow_html=True)
            col_t4a, col_t4b = st.columns(2)
            with col_t4a:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Mix Boston — % de Checks</div>\', unsafe_allow_html=True)
                mix = df_mf.groupby("type")["number_of_checks"].sum().reset_index()
                mix["pct"] = mix["number_of_checks"] / mix["number_of_checks"].sum() * 100
                fig_mix = go.Figure(go.Pie(
                    labels=mix["type"], values=mix["pct"].round(1),
                    marker_colors=[COR_BOSTON.get(t, MARROM) for t in mix["type"]],
                    textfont=dict(family="Nunito", size=12),
                    hole=0.4
                ))
                fig_mix.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10),
                    font=dict(family="Nunito"), height=260,
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM)))
                st.plotly_chart(fig_mix, use_container_width=True, key="fig_t4a_menu")
            with col_t4b:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Bebidas Puzzle — Qty/Check vs Meta</div>\', unsafe_allow_html=True)
                bebs_puzzle = ["SCHW TONICA", "SCHW CITRUS", "FANTA GUARANA"]
                df_bebs = df_mf[df_mf["item"].str.upper().str.contains("|".join(bebs_puzzle), na=False)]
                qty_atual = df_bebs["quantity_per_check"].mean() if len(df_bebs) > 0 else 0
                baseline = 1.11
                meta = 1.50
                pct_gauge = min((qty_atual - baseline) / (meta - baseline) * 100, 100) if qty_atual > baseline else 0
                cor_gauge = "#2e6b3e" if qty_atual >= meta else "#B8923A" if qty_atual >= baseline else VERMELHO
                st.markdown(
                    f\'<div style="text-align:center; padding:20px;">\'\
                    f\'<div style="font-size:48px; font-weight:800; color:{cor_gauge};">{qty_atual:.2f}</div>\'\
                    f\'<div style="font-size:12px; color:#8B7A5A; margin:8px 0;">un/check atual</div>\'\
                    f\'<div style="background:#e8ddc8; border-radius:8px; height:12px; margin:12px 0;">\'\
                    f\'<div style="background:{cor_gauge}; width:{max(pct_gauge,5):.0f}%; height:12px; border-radius:8px;"></div></div>\'\
                    f\'<div style="display:flex; justify-content:space-between; font-size:10px; color:#8B7A5A;">\'\
                    f\'<span>Baseline: {baseline}</span><span>Meta: {meta}</span></div></div>\',
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # TIER 5 — POS vs DELIVERY
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T5 — POS vs Delivery</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Dois canais com logicas e oportunidades distintas.</div>\', unsafe_allow_html=True)
            col_pos, col_dlv = st.columns(2)
            for col, canal_t5 in [(col_pos, "POS"), (col_dlv, "Delivery")]:
                df_canal = df_m[df_m["canal"] == canal_t5]
                df_canal = df_canal[df_canal["type"].isin(["Star","Dog","Puzzle","Horse"])]
                gross_c = df_canal["gross_sales"].sum()
                rev_c = df_canal["revenue_score"].sum()
                check_c = df_canal["ct_gross_total_check_avg"].mean()
                guest_c = df_canal["ct_guest_average"].mean()
                top5 = df_canal.sort_values("revenue_score", ascending=False).head(5)
                with col:
                    st.markdown(f\'<div style="font-size:13px; font-weight:800; color:#3D2B1F; margin-bottom:12px; text-align:center;">{canal_t5}</div>\', unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("Gross Sales", f"R$ {gross_c:,.0f}".replace(",","."))
                        st.metric("Check Medio", f"R$ {check_c:.0f}" if pd.notna(check_c) else "—")
                    with c2:
                        st.metric("Revenue Score", f"R$ {rev_c:,.0f}".replace(",","."))
                        st.metric("Guest Average", f"R$ {guest_c:.0f}" if pd.notna(guest_c) else "—")
                    st.markdown(\'<div style="font-size:10px; color:#8B7A5A; margin:8px 0;">TOP 5 por Revenue Score</div>\', unsafe_allow_html=True)
                    for _, r in top5.iterrows():
                        cor = COR_BOSTON.get(r["type"], MARROM)
                        st.markdown(
                            f\'<div style="display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid #e8ddc8;">\'\
                            f\'<span style="font-size:10px; color:#3D2B1F;">{r["item"][:28]}</span>\'\
                            f\'<span style="font-size:10px; font-weight:700; color:{cor};">{r["type"]}</span></div>\',
                            unsafe_allow_html=True
                        )
                    # Hero KPI Delivery
                    if canal_t5 == "Delivery":
                        puzz_dlv = df_canal[df_canal["type"]=="Puzzle"]["ct_guest_average"].mean()
                        if pd.notna(puzz_dlv):
                            st.markdown(
                                f\'<div style="background:#1a1209; border-radius:8px; padding:12px; margin-top:12px; border:1px solid #8B9A2E; text-align:center;">\'\
                                f\'<div style="font-size:9px; color:#8B9A2E; letter-spacing:2px;">GUEST AVG PUZZLES DELIVERY</div>\'\
                                f\'<div style="font-size:32px; font-weight:800; color:#8B9A2E;">R$ {puzz_dlv:.0f}</div>\'\
                                f\'<div style="font-size:9px; color:#8B7A5A;">maior do portfolio</div></div>\',
                                unsafe_allow_html=True
                            )

        st.markdown("<br>", unsafe_allow_html=True)

        # TIER 6 — TEMPO
        with st.container(border=True):
            st.markdown(\'<div class="section-title">T6 — Tempo: Dia e Turno</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Concentracao de receita por dia e turno — onde estao as oportunidades.</div>\', unsafe_allow_html=True)
            col_t6a, col_t6b = st.columns(2)
            with col_t6a:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Gross Sales por Dia mais Popular</div>\', unsafe_allow_html=True)
                df_dia = df_mf.copy()
                df_dia["dia"] = df_dia["most_popular_day"].str.split(" ").str[0]
                dias_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
                dias_label = ["Seg","Ter","Qua","Qui","Sex","Sab","Dom"]
                dia_gross = df_dia.groupby("dia")["gross_sales"].sum().reindex(dias_order).reset_index()
                dia_gross.columns = ["dia","gross"]
                dia_gross["label"] = dia_gross["dia"].map(dict(zip(dias_order, dias_label)))
                fig_dia = go.Figure(go.Bar(
                    x=dia_gross["label"], y=dia_gross["gross"],
                    marker_color=[VERDE if d in ["Saturday","Sunday"] else "#8B7A5A" for d in dia_gross["dia"]],
                    text=dia_gross["gross"].apply(lambda v: f"R$ {v/1000:.0f}k" if pd.notna(v) else ""),
                    textposition="outside", textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_dia.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_dia, use_container_width=True, key="fig_t6a_menu")
            with col_t6b:
                st.markdown(\'<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Gross Sales por Turno</div>\', unsafe_allow_html=True)
                df_turno = df_mf.copy()
                df_turno["turno"] = df_turno["most_popular_day_part"].str.split(" ").str[0]
                turno_gross = df_turno.groupby("turno")["gross_sales"].sum().reset_index()
                fig_turno = go.Figure(go.Pie(
                    labels=turno_gross["turno"], values=turno_gross["gross_sales"].round(0),
                    marker_colors=[VERDE, "#B8923A", "#8B7A5A"],
                    textfont=dict(family="Nunito", size=12), hole=0.4
                ))
                fig_turno.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    font=dict(family="Nunito"), height=260,
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM)))
                st.plotly_chart(fig_turno, use_container_width=True, key="fig_t6b_menu")

            st.markdown(\'<div style="font-size:11px; color:#8B7A5A; margin-top:8px;">💡 73%% dos itens picam em Sab ou Dom. Puzzles tem proporcionalmente mais peso no Domingo — janela de exploracao.</div>\', unsafe_allow_html=True)

'''

old = 'st.markdown(\n    \'<div style="text-align:center; font-size:10px; color:#B8A898; letter-spacing:0.1em; padding-top:20px;">\''
new = menu_block + 'st.markdown(\n    \'<div style="text-align:center; font-size:10px; color:#B8A898; letter-spacing:0.1em; padding-top:20px;">\''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK bloco menu adicionado')
else:
    print('TRECHO NAO ENCONTRADO')
