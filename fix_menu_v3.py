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
            st.markdown(f\'<div style="font-size:11px; color:#8B7A5A; padding-top:28px;">📅 Referencia: {semana_sel} | Semana {len(semanas_disp)} de historico</div>\', unsafe_allow_html=True)

        df_mf = df_m.copy()
        if canal_sel != "Ambos":
            df_mf = df_mf[df_mf["canal"] == canal_sel]
        if tipo_sel != "Todos":
            df_mf = df_mf[df_mf["type"] == tipo_sel]

        COR_BOSTON = {"Star": "#B8923A", "Dog": VERMELHO, "Puzzle": "#4A90D9", "Horse": VERDE}

        def card_lia(leitura, insight, acao):
            return (
                \'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:12px;">\' +
                \'<div style="background:#e8f2eb; border-radius:8px; padding:12px;">\' +
                \'<div style="font-size:9px; font-weight:700; color:#2e6b3e; letter-spacing:2px; margin-bottom:5px;">📊 LEITURA</div>\' +
                f\'<div style="font-size:11px; color:#3D2B1F; line-height:1.5;">{leitura}</div></div>\' +
                \'<div style="background:#fdf5e6; border-radius:8px; padding:12px;">\' +
                \'<div style="font-size:9px; font-weight:700; color:#B8923A; letter-spacing:2px; margin-bottom:5px;">💡 INSIGHT</div>\' +
                f\'<div style="font-size:11px; color:#3D2B1F; line-height:1.5;">{insight}</div></div>\' +
                \'<div style="background:#e8f0f8; border-radius:8px; padding:12px;">\' +
                \'<div style="font-size:9px; font-weight:700; color:#4A90D9; letter-spacing:2px; margin-bottom:5px;">🎯 ACAO</div>\' +
                f\'<div style="font-size:11px; color:#3D2B1F; line-height:1.5;">{acao}</div></div></div>\'
            )

        stars = df_mf[df_mf["type"]=="Star"]
        dogs = df_mf[df_mf["type"]=="Dog"]
        puzzles = df_mf[df_mf["type"]=="Puzzle"]
        horses = df_mf[df_mf["type"]=="Horse"]
        gross_total = df_mf["gross_sales"].sum() if df_mf["gross_sales"].sum() > 0 else 1
        rev_total = df_mf["revenue_score"].sum() if df_mf["revenue_score"].sum() > 0 else 1
        checks_total = int(df_mf["number_of_checks"].sum()) if df_mf["number_of_checks"].sum() > 0 else 1
        df_bebs = df_mf[df_mf["item"].str.upper().str.contains("SCHW TONICA|SCHW CITRUS|FANTA GUARANA", na=False)]
        qty_bebs = df_bebs["quantity_per_check"].mean() if len(df_bebs) > 0 else 0

        # PAINEL EXECUTIVO
        st.markdown("<br>", unsafe_allow_html=True)
        col_e1, col_e2, col_e3, col_e4 = st.columns(4)
        with col_e1:
            with st.container(border=True):
                pct_star_g = stars["gross_sales"].sum()/gross_total*100
                st.markdown(
                    \'<div style="text-align:center; padding:8px;">\' +
                    \'<div style="font-size:9px; color:#8B7A5A; letter-spacing:2px; margin-bottom:4px;">GROSS SALES</div>\' +
                    f\'<div style="font-size:28px; font-weight:800; color:#3D2B1F;">R$ {gross_total/1000:.0f}k</div>\' +
                    f\'<div style="font-size:10px; color:#8B9A2E;">{pct_star_g:.0f}% Stars</div></div>\',
                    unsafe_allow_html=True)
        with col_e2:
            with st.container(border=True):
                st.markdown(
                    \'<div style="text-align:center; padding:8px;">\' +
                    \'<div style="font-size:9px; color:#8B7A5A; letter-spacing:2px; margin-bottom:4px;">REVENUE SCORE</div>\' +
                    f\'<div style="font-size:28px; font-weight:800; color:#3D2B1F;">R$ {rev_total/1000:.0f}k</div>\' +
                    f\'<div style="font-size:10px; color:#8B9A2E;">impacto real na receita</div></div>\',
                    unsafe_allow_html=True)
        with col_e3:
            with st.container(border=True):
                pct_stars_mix = stars["number_of_checks"].sum()/checks_total*100
                pct_dogs_mix = dogs["number_of_checks"].sum()/checks_total*100
                cor_mix = "#2e6b3e" if pct_stars_mix >= 60 else "#B8923A"
                st.markdown(
                    \'<div style="text-align:center; padding:8px;">\' +
                    \'<div style="font-size:9px; color:#8B7A5A; letter-spacing:2px; margin-bottom:4px;">MIX BOSTON</div>\' +
                    f\'<div style="font-size:28px; font-weight:800; color:{cor_mix};">{pct_stars_mix:.0f}% ⭐</div>\' +
                    f\'<div style="font-size:10px; color:#8B7A5A;">{pct_dogs_mix:.0f}% Dogs no mix</div></div>\',
                    unsafe_allow_html=True)
        with col_e4:
            with st.container(border=True):
                baseline_beb = 1.11
                meta_beb = 1.50
                cor_beb = "#2e6b3e" if qty_bebs >= meta_beb else "#B8923A" if qty_bebs >= baseline_beb else VERMELHO
                st.markdown(
                    \'<div style="text-align:center; padding:8px;">\' +
                    \'<div style="font-size:9px; color:#8B7A5A; letter-spacing:2px; margin-bottom:4px;">BEBIDAS PUZZLE</div>\' +
                    f\'<div style="font-size:28px; font-weight:800; color:{cor_beb};">{qty_bebs:.2f}</div>\' +
                    f\'<div style="font-size:10px; color:#8B7A5A;">un/check | meta {meta_beb}</div></div>\',
                    unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 1 — MATRIZ BOSTON
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Matriz Boston — Visao Completa da Semana</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Todos os itens num unico visual. Eixo X = volume de pedidos, Eixo Y = Revenue Score, tamanho = Gross Sales.</div>\', unsafe_allow_html=True)
            df_scatter = df_mf[df_mf["revenue_score"].notna() & df_mf["number_of_checks"].notna()].copy()
            fig_scatter = go.Figure()
            for tipo in ["Star","Dog","Puzzle","Horse"]:
                df_tipo = df_scatter[df_scatter["type"]==tipo]
                if len(df_tipo) == 0:
                    continue
                fig_scatter.add_trace(go.Scatter(
                    x=df_tipo["number_of_checks"],
                    y=df_tipo["revenue_score"],
                    mode="markers+text",
                    name=tipo,
                    marker=dict(
                        size=df_tipo["gross_sales"].apply(lambda v: max(8, min(40, v/15000))),
                        color=COR_BOSTON.get(tipo, MARROM),
                        opacity=0.8,
                        line=dict(width=1, color="white")
                    ),
                    text=df_tipo["item"].str[:18],
                    textposition="top center",
                    textfont=dict(family="Nunito", size=7, color=MARROM),
                    hovertemplate=(
                        "<b>%{text}</b><br>" +
                        "Checks: %{x}<br>" +
                        "Revenue Score: R$ %{y:,.0f}<br>" +
                        "<extra></extra>"
                    )
                ))
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=40,l=60,r=10),
                xaxis=dict(title="Numero de Checks", showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                yaxis=dict(title="Revenue Score (R$)", showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                font=dict(family="Nunito"), height=480
            )
            st.plotly_chart(fig_scatter, use_container_width=True, key="fig_scatter_menu")
            dog_check_avg = dogs["ct_gross_total_check_avg"].mean() if len(dogs)>0 else 0
            star_check_avg = stars["ct_gross_total_check_avg"].mean() if len(stars)>0 else 0
            top_dog = dogs.sort_values("number_of_checks", ascending=False).iloc[0] if len(dogs)>0 else None
            top_puzzle = puzzles.sort_values("revenue_score", ascending=False).iloc[0] if len(puzzles)>0 else None
            leitura = f"Stars dominam o volume com {int(stars['number_of_checks'].sum()):,} checks ({stars['number_of_checks'].sum()/checks_total*100:.0f}% do total). Dogs tem {int(dogs['number_of_checks'].sum()):,} checks mas Revenue Score concentrado abaixo dos Stars. Puzzles sao poucos e pequenos — alta margem, baixa visibilidade."
            insight = f"Dogs tem check completo medio R$ {dog_check_avg:.0f} vs Stars R$ {star_check_avg:.0f}. Quando o cliente pede um Dog, a mesa gasta mais. O problema nao e o cliente — e o posicionamento do item." + (f" {top_puzzle['item']} e o Puzzle com maior Revenue Score — candidato a promocao de visibilidade." if top_puzzle is not None else "")
            acao = f"Priorizar os Dogs com maior numero de checks e check completo acima de R$ 280 para revisao de posicionamento no cardapio. Criar acao de visibilidade para Puzzles com Revenue Score acima de R$ 50k."
            st.markdown(card_lia(leitura, insight, acao), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 2 — DOGS COM POTENCIAL OCULTO
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Dogs com Potencial Oculto</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Itens classificados como Dog mas com comportamento de mesa acima da media — candidatos a reposicionamento.</div>\', unsafe_allow_html=True)
            df_dogs_pot = dogs.copy()
            df_dogs_pot = df_dogs_pot[df_dogs_pot["ct_gross_total_check_avg"].notna()]
            df_dogs_pot = df_dogs_pot.sort_values("ct_gross_total_check_avg", ascending=False).head(8)
            if len(df_dogs_pot) > 0:
                media_check_geral = df_mf["ct_gross_total_check_avg"].mean()
                for _, row in df_dogs_pot.iterrows():
                    delta_check = row["ct_gross_total_check_avg"] - media_check_geral
                    cor_delta = "#2e6b3e" if delta_check > 0 else VERMELHO
                    sinal = "+" if delta_check > 0 else ""
                    canal_icon = "🛵" if row["canal"] == "Delivery" else "🍽️"
                    st.markdown(
                        f\'<div style="display:flex; align-items:center; padding:10px 0; border-bottom:1px solid #e8ddc8; gap:16px;">\' +
                        f\'<div style="width:28px; font-size:16px; text-align:center;">{canal_icon}</div>\' +
                        f\'<div style="flex:2; font-size:12px; font-weight:700; color:#3D2B1F;">{row["item"]}</div>\' +
                        f\'<div style="flex:1; text-align:center;">\' +
                        f\'<div style="font-size:9px; color:#8B7A5A;">CHECKS</div>\' +
                        f\'<div style="font-size:13px; font-weight:700; color:#3D2B1F;">{int(row["number_of_checks"]):,}</div></div>\' +
                        f\'<div style="flex:1; text-align:center;">\' +
                        f\'<div style="font-size:9px; color:#8B7A5A;">CHECK COMPLETO</div>\' +
                        f\'<div style="font-size:13px; font-weight:700; color:{cor_delta};">R$ {row["ct_gross_total_check_avg"]:.0f} ({sinal}R$ {abs(delta_check):.0f} vs media)</div></div>\' +
                        f\'<div style="flex:1; text-align:center;">\' +
                        f\'<div style="font-size:9px; color:#8B7A5A;">GROSS SALES</div>\' +
                        f\'<div style="font-size:13px; font-weight:700; color:#3D2B1F;">R$ {row["gross_sales"]:,.0f}".replace(",",".")</div></div></div>\',
                        unsafe_allow_html=True
                    )
                melhor_dog = df_dogs_pot.iloc[0]
                st.markdown(card_lia(
                    leitura=f"{len(df_dogs_pot)} Dogs tem check completo acima da media geral (R$ {media_check_geral:.0f}). Lider: {melhor_dog['item']} com check de R$ {melhor_dog['ct_gross_total_check_avg']:.0f} e {int(melhor_dog['number_of_checks']):,} pedidos.",
                    insight="Dogs com check completo alto indicam que quando esse item esta na mesa, o cliente gasta mais — em outras entradas, bebidas e sobremesas. A baixa classificacao Boston e resultado de baixa margem ou baixo volume, nao de comportamento do cliente.",
                    acao=f"Revisar precificacao e posicionamento dos top 3 Dogs por check completo. Avaliar inclusao no script de sugestao ativa do garcom como opcao alternativa aos Stars mais caros."
                ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 3 — BEBIDAS PUZZLE
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Bebidas Puzzle — Evolucao do Script de Sugestao Ativa</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Schw Tonica + Schw Citrus + Fanta Guarana. Meta: 1,50 un/check (baseline: 1,11).</div>\', unsafe_allow_html=True)
            col_b1, col_b2 = st.columns([1,2])
            with col_b1:
                pct_g = min((qty_bebs-baseline_beb)/(meta_beb-baseline_beb)*100,100) if qty_bebs>baseline_beb else 0
                cor_g = "#2e6b3e" if qty_bebs>=meta_beb else "#B8923A" if qty_bebs>=baseline_beb else VERMELHO
                status_g = "✅ Meta atingida!" if qty_bebs>=meta_beb else f"Faltam {meta_beb-qty_bebs:.2f} un/check"
                st.markdown(
                    f\'<div style="text-align:center; padding:20px;">\' +
                    f\'<div style="font-size:64px; font-weight:800; color:{cor_g}; line-height:1;">{qty_bebs:.2f}</div>\' +
                    f\'<div style="font-size:12px; color:#8B7A5A; margin:6px 0;">un/check atual</div>\' +
                    f\'<div style="background:#e8ddc8; border-radius:8px; height:12px; margin:16px 0;">\' +
                    f\'<div style="background:{cor_g}; width:{max(pct_g,3):.0f}%; height:12px; border-radius:8px;"></div></div>\' +
                    f\'<div style="display:flex; justify-content:space-between; font-size:10px; color:#8B7A5A; margin-bottom:8px;">\' +
                    f\'<span>Baseline: {baseline_beb}</span><span>Meta: {meta_beb}</span></div>\' +
                    f\'<div style="font-size:13px; font-weight:700; color:{cor_g};">{status_g}</div></div>\',
                    unsafe_allow_html=True)
            with col_b2:
                if len(semanas_disp) > 1:
                    df_bebs_hist = df_menu[~df_menu["item"].str.upper().isin(["BROWNIE CORTESIA","SSB"])]
                    df_bebs_hist = df_bebs_hist[df_bebs_hist["item"].str.upper().str.contains("SCHW TONICA|SCHW CITRUS|FANTA GUARANA", na=False)]
                    evo_bebs = df_bebs_hist.groupby("semana_ref")["quantity_per_check"].mean().reset_index().sort_values("semana_ref")
                    fig_bebs = go.Figure()
                    fig_bebs.add_hline(y=baseline_beb, line_dash="dot", line_color="#8B7A5A", annotation_text=f"Baseline {baseline_beb}", annotation_font=dict(size=10))
                    fig_bebs.add_hline(y=meta_beb, line_dash="dash", line_color="#2e6b3e", annotation_text=f"Meta {meta_beb}", annotation_font=dict(size=10))
                    fig_bebs.add_trace(go.Scatter(
                        x=evo_bebs["semana_ref"].astype(str), y=evo_bebs["quantity_per_check"],
                        mode="lines+markers+text",
                        line=dict(color="#4A90D9", width=3),
                        marker=dict(size=10, color="#4A90D9"),
                        text=evo_bebs["quantity_per_check"].round(2),
                        textposition="top center",
                        textfont=dict(family="Nunito", size=11)
                    ))
                    fig_bebs.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(t=20,b=10,l=10,r=10),
                        xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM), showgrid=False),
                        yaxis=dict(range=[0.8, 1.8], showgrid=True, gridcolor="#E8DCC8"),
                        font=dict(family="Nunito"), height=260)
                    st.plotly_chart(fig_bebs, use_container_width=True, key="fig_bebs_menu")
                else:
                    st.markdown(
                        \'<div style="background:#f5f0e8; border-radius:12px; padding:30px; text-align:center; margin:10px;">\' +
                        \'<div style="font-size:32px; margin-bottom:12px;">📈</div>\' +
                        \'<div style="font-size:13px; font-weight:700; color:#3D2B1F; margin-bottom:8px;">Semana 1 de historico registrada</div>\' +
                        \'<div style="font-size:11px; color:#8B7A5A;">O grafico de evolucao aparecera automaticamente<br>quando a semana 2 for importada.</div></div>\',
                        unsafe_allow_html=True)
            st.markdown(card_lia(
                leitura=f"Bebidas Puzzle em {qty_bebs:.2f} un/check — {'na baseline' if abs(qty_bebs-baseline_beb)<0.05 else 'acima da baseline' if qty_bebs>baseline_beb else 'abaixo da baseline'}. Fanta Guarana lidera em checks ({int(df_bebs['number_of_checks'].sum()):,} pedidos). {len(semanas_disp)} semana(s) de historico disponivel.",
                insight="Qty/check abaixo de 1,50 indica que o script de sugestao ativa ainda nao esta sistematico. A meta de 1,50 representa +35% vs baseline — alcancavel com script estruturado e treinamento.",
                acao="Implementar script padrao de sugestao em todos os turnos. Monitorar semana a semana — o grafico de evolucao mostrara o impacto do treinamento em tempo real."
            ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 4 — POS vs DELIVERY
        with st.container(border=True):
            st.markdown(\'<div class="section-title">POS vs Delivery — Dois Canais, Duas Estrategias</div>\', unsafe_allow_html=True)
            gross_pos = df_m[df_m["canal"]=="POS"]["gross_sales"].sum()
            gross_dlv = df_m[df_m["canal"]=="Delivery"]["gross_sales"].sum()
            pct_dlv = gross_dlv/(gross_pos+gross_dlv)*100 if (gross_pos+gross_dlv)>0 else 0
            guest_pos_m = df_m[df_m["canal"]=="POS"]["ct_guest_average"].mean()
            guest_dlv_m = df_m[df_m["canal"]=="Delivery"]["ct_guest_average"].mean()
            st.markdown(
                f\'<div style="background:#3D2B1F; border-radius:8px; padding:14px 20px; margin-bottom:16px; border-left:4px solid #4A90D9;">\' +
                f\'<span style="font-size:13px; color:#F5F0E8;">🔑 <b>Headline:</b> Delivery representa apenas <b style="color:#4A90D9;">{pct_dlv:.1f}% do Gross Sales</b> mas tem Guest Average de <b style="color:#8B9A2E;">R$ {guest_dlv_m:.0f}</b> vs R$ {guest_pos_m:.0f} no POS — <b>o cliente de delivery e mais valioso por pessoa.</b></span></div>\',
                unsafe_allow_html=True)
            col_pos, col_dlv_c = st.columns(2)
            for col_c, canal_t5 in [(col_pos,"POS"),(col_dlv_c,"Delivery")]:
                df_canal = df_m[df_m["canal"]==canal_t5]
                df_canal = df_canal[df_canal["type"].isin(["Star","Dog","Puzzle","Horse"])]
                gross_c = df_canal["gross_sales"].sum()
                check_c = df_canal["ct_gross_total_check_avg"].mean()
                guest_c = df_canal["ct_guest_average"].mean()
                top5 = df_canal.sort_values("revenue_score", ascending=False).head(5)
                puzz_c = df_canal[df_canal["type"]=="Puzzle"]
                with col_c:
                    icon = "🍽️" if canal_t5=="POS" else "🛵"
                    st.markdown(f\'<div style="font-size:14px; font-weight:800; color:#3D2B1F; margin-bottom:12px; padding-bottom:8px; border-bottom:2px solid {"#8B9A2E" if canal_t5=="POS" else "#4A90D9"};">{icon} {canal_t5}</div>\', unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Gross", f"R$ {gross_c/1000:.0f}k")
                    with c2:
                        st.metric("Check Medio", f"R$ {check_c:.0f}" if pd.notna(check_c) else "—")
                    with c3:
                        st.metric("Guest Avg", f"R$ {guest_c:.0f}" if pd.notna(guest_c) else "—")
                    st.markdown(\'<div style="font-size:10px; color:#8B7A5A; margin:8px 0 4px 0; font-weight:700;">TOP 5 POR REVENUE SCORE</div>\', unsafe_allow_html=True)
                    for _, r in top5.iterrows():
                        cor = COR_BOSTON.get(r["type"], MARROM)
                        st.markdown(
                            f\'<div style="display:flex; justify-content:space-between; align-items:center; padding:5px 0; border-bottom:1px solid #e8ddc8;">\' +
                            f\'<span style="font-size:10px; color:#3D2B1F;">{r["item"][:26]}</span>\' +
                            f\'<span style="font-size:9px; font-weight:700; color:{cor}; background:{cor}22; padding:2px 6px; border-radius:4px;">{r["type"]}</span></div>\',
                            unsafe_allow_html=True)
                    if canal_t5=="Delivery" and len(puzz_c)>0:
                        puzz_guest = puzz_c["ct_guest_average"].mean()
                        if pd.notna(puzz_guest) and puzz_guest>0:
                            st.markdown(
                                f\'<div style="background:#1a1209; border-radius:8px; padding:10px; margin-top:10px; border:1px solid #8B9A2E; text-align:center;">\' +
                                f\'<div style="font-size:9px; color:#8B9A2E; letter-spacing:2px; margin-bottom:2px;">GUEST AVG PUZZLES DELIVERY</div>\' +
                                f\'<div style="font-size:30px; font-weight:800; color:#8B9A2E;">R$ {puzz_guest:.0f}</div>\' +
                                f\'<div style="font-size:9px; color:#8B7A5A;">maior guest average do portfolio</div></div>\',
                                unsafe_allow_html=True)
            st.markdown(card_lia(
                leitura=f"POS: R$ {gross_pos/1000:.0f}k gross ({100-pct_dlv:.0f}% do total). Delivery: R$ {gross_dlv/1000:.0f}k ({pct_dlv:.1f}%). Guest Average delivery R$ {guest_dlv_m:.0f} vs R$ {guest_pos_m:.0f} no POS.",
                insight="Delivery e menor em volume mas mais eficiente por pessoa. Puzzles delivery tem o maior guest average do portfolio — quem pede Puzzle no app gasta mais em tudo.",
                acao="Criar bundle exclusivo de Puzzles para Delivery. Revisar posicionamento dos Puzzles no topo do cardapio do iFood — pequena mudanca de visibilidade com grande impacto em Revenue Score."
            ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 5 — EVOLUCAO (RESERVADO)
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Evolucao Semanal — Revenue Score por Tipo Boston</div>\', unsafe_allow_html=True)
            if len(semanas_disp) > 1:
                df_evo = df_menu[df_menu["type"].isin(["Star","Dog","Puzzle","Horse"])].copy()
                df_evo = df_evo[~df_evo["item"].str.upper().isin(["BROWNIE CORTESIA","SSB"])]
                df_evo = df_evo[~df_evo["item"].str.upper().str.startswith("RF ")]
                evo_tipo = df_evo.groupby(["semana_ref","type"])["revenue_score"].sum().reset_index()
                fig_evo = go.Figure()
                for tipo in ["Star","Dog","Puzzle","Horse"]:
                    df_t = evo_tipo[evo_tipo["type"]==tipo].sort_values("semana_ref")
                    if len(df_t) > 0:
                        fig_evo.add_trace(go.Scatter(
                            x=df_t["semana_ref"].astype(str),
                            y=df_t["revenue_score"],
                            mode="lines+markers",
                            name=tipo,
                            line=dict(color=COR_BOSTON.get(tipo, MARROM), width=2),
                            marker=dict(size=8, color=COR_BOSTON.get(tipo, MARROM))
                        ))
                fig_evo.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM), showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10)),
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                    font=dict(family="Nunito"), height=300)
                st.plotly_chart(fig_evo, use_container_width=True, key="fig_evo_menu")
            else:
                st.markdown(
                    \'<div style="background:#f5f0e8; border-radius:12px; padding:40px; text-align:center;">\' +
                    \'<div style="font-size:40px; margin-bottom:16px;">📊</div>\' +
                    \'<div style="font-size:15px; font-weight:700; color:#3D2B1F; margin-bottom:8px;">Semana 1 de historico registrada</div>\' +
                    \'<div style="font-size:12px; color:#8B7A5A; line-height:1.6;">Este grafico mostrara a evolucao do Revenue Score por tipo Boston semana a semana.<br>Importe a proxima semana para ver a tendencia aparecer.</div>\' +
                    f\'<div style="margin-top:16px; font-size:11px; color:#8B9A2E; font-weight:700;">Proxima atualizacao esperada: segunda-feira</div></div>\',
                    unsafe_allow_html=True)
            st.markdown(card_lia(
                leitura=f"{len(semanas_disp)} semana(s) de historico disponivel. Revenue Score atual: Stars R$ {stars['revenue_score'].sum()/1000:.0f}k | Dogs R$ {dogs['revenue_score'].sum()/1000:.0f}k | Puzzles R$ {puzzles['revenue_score'].sum()/1000:.0f}k.",
                insight="Revenue Score por tipo e o indicador-chave do Menu Engineering — mostra se a estrategia esta migrando receita de Dogs para Stars e aumentando a contribuicao de Puzzles ao longo do tempo.",
                acao="Importar o arquivo toda segunda-feira apos receber o relatorio. Em 4 semanas o grafico ja mostrara tendencias claras de evolucao do mix."
            ), unsafe_allow_html=True)

'''

result = content[:start] + novo + content[end:]
open('dashboard.py', 'w', encoding='utf-8').write(result)
print(f'OK — {len(result.splitlines())} linhas')
