lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

novo = '''if aba_sel == "Reviews":
    st.markdown(\'<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Reviews & Reputacao</div>\', unsafe_allow_html=True)

    df_recl = df_reclamacoes.copy()
    df_recl["data"] = pd.to_datetime(df_recl["data"])

    # Filtros
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        unidades_disp = ["Todas"] + sorted(df_recl["unidade_curta"].dropna().unique().tolist())
        unidade_recl = st.selectbox("Unidade:", unidades_disp, key="recl_unidade")
    with col_f2:
        temas_disp = ["Todos"] + sorted(df_recl["tema"].dropna().unique().tolist())
        tema_recl = st.selectbox("Tema:", temas_disp, key="recl_tema")
    with col_f3:
        canais_disp = ["Todos"] + sorted(df_recl["canal"].dropna().unique().tolist())
        canal_recl = st.selectbox("Canal:", canais_disp, key="recl_canal")

    df_rf = df_recl.copy()
    if unidade_recl != "Todas":
        df_rf = df_rf[df_rf["unidade_curta"] == unidade_recl]
    if tema_recl != "Todos":
        df_rf = df_rf[df_rf["tema"] == tema_recl]
    if canal_recl != "Todos":
        df_rf = df_rf[df_rf["canal"] == canal_recl]

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 1 — RADAR DA REDE
    with st.container(border=True):
        st.markdown(\'<div class="section-title">Radar da Rede</div>\', unsafe_allow_html=True)
        total_recl = len(df_rf)
        data_min = df_rf["data"].min()
        data_max = df_rf["data"].max()
        meses_periodo = max(1, ((data_max - data_min).days / 30)) if pd.notna(data_min) and pd.notna(data_max) else 1
        recl_mes = total_recl / meses_periodo
        nota_media = df_rf["avaliacao"].mean() if df_rf["avaliacao"].notna().any() else 0
        pct_google = len(df_rf[df_rf["canal"]=="google_my_business"]) / total_recl * 100 if total_recl > 0 else 0
        tema_top = df_rf["tema"].value_counts().index[0] if len(df_rf) > 0 and df_rf["tema"].notna().any() else "—"
        col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns(5)
        with col_r1:
            st.metric("Reclamacoes", total_recl)
        with col_r2:
            st.metric("Recl./Mes", f"{recl_mes:.1f}")
        with col_r3:
            cor_nota = "#2e6b3e" if nota_media >= 3 else "#B8923A" if nota_media >= 2 else VERMELHO
            st.markdown(f\'<div style="text-align:center;"><div style="font-size:12px;color:#8B7A5A;">Nota Media</div><div style="font-size:24px;font-weight:700;color:{cor_nota};">{nota_media:.2f}</div></div>\', unsafe_allow_html=True)
        with col_r4:
            st.metric("Via Google", f"{pct_google:.0f}%")
        with col_r5:
            st.metric("Tema #1", tema_top)

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 2 — COMPARATIVO POR UNIDADE
    with st.container(border=True):
        st.markdown(\'<div class="section-title">Comparativo por Unidade</div>\', unsafe_allow_html=True)
        unidades_ord = ["Morumbi","Center Norte","Dom Pedro","Aricanduva","Guarulhos GRU3","Guarulhos GRU2"]
        rows_tab = []
        for un in unidades_ord:
            df_un = df_recl[df_recl["unidade_curta"]==un]
            if len(df_un) == 0:
                continue
            n = len(df_un)
            d_min = df_un["data"].min()
            d_max = df_un["data"].max()
            meses_un = max(1, (d_max - d_min).days / 30)
            rpm = n / meses_un
            nota_un = df_un["avaliacao"].mean() if df_un["avaliacao"].notna().any() else 0
            tema_un = df_un["tema"].value_counts().index[0] if df_un["tema"].notna().any() else "—"
            subtema_un = df_un["subtema"].value_counts().index[0] if df_un["subtema"].notna().any() else "—"
            rows_tab.append({"Unidade": un, "Recl.": n, "Recl./Mes": f"{rpm:.1f}", "Nota": nota_un, "Tema #1": tema_un, "Dor Principal": subtema_un})
        df_tab_un = pd.DataFrame(rows_tab)
        for _, row in df_tab_un.iterrows():
            nota_v = row["Nota"]
            cor_n = "#2e6b3e" if nota_v >= 3 else "#B8923A" if nota_v >= 2 else VERMELHO
            st.markdown(
                f\'<div style="display:flex;align-items:center;padding:10px 0;border-bottom:1px solid #e8ddc8;gap:12px;">\' +
                f\'<div style="flex:2;font-size:12px;font-weight:700;color:#3D2B1F;">{row["Unidade"]}</div>\' +
                f\'<div style="flex:1;text-align:center;"><div style="font-size:9px;color:#8B7A5A;">RECL.</div><div style="font-size:14px;font-weight:700;color:#3D2B1F;">{row["Recl."]}</div></div>\' +
                f\'<div style="flex:1;text-align:center;"><div style="font-size:9px;color:#8B7A5A;">RECL./MES</div><div style="font-size:14px;font-weight:700;color:#3D2B1F;">{row["Recl./Mes"]}</div></div>\' +
                f\'<div style="flex:1;text-align:center;"><div style="font-size:9px;color:#8B7A5A;">NOTA</div><div style="font-size:14px;font-weight:700;color:{cor_n};">{nota_v:.2f}</div></div>\' +
                f\'<div style="flex:2;text-align:center;"><div style="font-size:9px;color:#8B7A5A;">TEMA #1</div><div style="font-size:11px;color:#3D2B1F;">{row["Tema #1"]}</div></div>\' +
                f\'<div style="flex:3;"><div style="font-size:9px;color:#8B7A5A;">DOR PRINCIPAL</div><div style="font-size:11px;color:#3D2B1F;">{row["Dor Principal"]}</div></div></div>\',
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 3 — EVOLUCAO MENSAL
    with st.container(border=True):
        st.markdown(\'<div class="section-title">Evolucao Mensal de Reclamacoes</div>\', unsafe_allow_html=True)
        df_evo_recl = df_rf.copy()
        df_evo_recl["mes"] = df_evo_recl["data"].dt.to_period("M").astype(str)
        cores_un = {"Morumbi":"#B8923A","Center Norte":"#4A90D9","Dom Pedro":"#2e6b3e","Aricanduva":"#c0392b","Guarulhos GRU3":"#8B7A5A","Guarulhos GRU2":"#9B59B6"}
        fig_evo_recl = go.Figure()
        for un in unidades_ord:
            df_un_evo = df_evo_recl[df_evo_recl["unidade_curta"]==un].groupby("mes").size().reset_index(name="n")
            if len(df_un_evo) == 0:
                continue
            fig_evo_recl.add_trace(go.Scatter(
                x=df_un_evo["mes"], y=df_un_evo["n"],
                mode="lines+markers", name=un,
                line=dict(color=cores_un.get(un, MARROM), width=2),
                marker=dict(size=7, color=cores_un.get(un, MARROM))
            ))
        fig_evo_recl.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10,b=10,l=10,r=10),
            xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM), showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
            legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
            font=dict(family="Nunito"), height=300
        )
        st.plotly_chart(fig_evo_recl, use_container_width=True, key="fig_evo_recl")

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 4 — MIX DE TEMAS
    with st.container(border=True):
        st.markdown(\'<div class="section-title">Mix de Temas</div>\', unsafe_allow_html=True)
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Rede Geral</div>\', unsafe_allow_html=True)
            temas_rede = df_rf["tema"].value_counts().reset_index()
            temas_rede.columns = ["tema","n"]
            fig_temas = go.Figure(go.Bar(
                y=temas_rede["tema"], x=temas_rede["n"],
                orientation="h",
                marker_color=[VERDE if i==0 else "#B8923A" if i==1 else "#8B7A5A" for i in range(len(temas_rede))],
                text=temas_rede["n"], textposition="outside",
                textfont=dict(family="Nunito", size=10, color=MARROM)
            ))
            fig_temas.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)),
                font=dict(family="Nunito"), height=280)
            st.plotly_chart(fig_temas, use_container_width=True, key="fig_temas_recl")
        with col_t2:
            st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Subtemas — Top 10</div>\', unsafe_allow_html=True)
            subtemas_rede = df_rf["subtema"].dropna().value_counts().head(10).reset_index()
            subtemas_rede.columns = ["subtema","n"]
            fig_sub = go.Figure(go.Bar(
                y=subtemas_rede["subtema"], x=subtemas_rede["n"],
                orientation="h",
                marker_color=VERMELHO,
                text=subtemas_rede["n"], textposition="outside",
                textfont=dict(family="Nunito", size=10, color=MARROM)
            ))
            fig_sub.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)),
                font=dict(family="Nunito"), height=280)
            st.plotly_chart(fig_sub, use_container_width=True, key="fig_sub_recl")

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 5 — VOZ DO CLIENTE
    with st.container(border=True):
        st.markdown(\'<div class="section-title">Voz do Cliente</div>\', unsafe_allow_html=True)
        st.markdown(\'<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Reclamacoes reais — filtradas por unidade, tema e canal acima.</div>\', unsafe_allow_html=True)
        df_voz = df_rf.sort_values("data", ascending=False).head(50)
        for _, row in df_voz.iterrows():
            nota_v = row["avaliacao"]
            cor_nota_v = "#2e6b3e" if pd.notna(nota_v) and nota_v >= 3 else "#B8923A" if pd.notna(nota_v) and nota_v >= 2 else VERMELHO
            estrelas = "★" * int(nota_v) if pd.notna(nota_v) else "—"
            canal_icon = "📱" if row["canal"] == "instagram" else "🔍"
            tema_badge = row["tema"] if pd.notna(row["tema"]) else ""
            subtema_badge = row["subtema"] if pd.notna(row["subtema"]) else ""
            st.markdown(
                f\'<div style="padding:12px 0;border-bottom:1px solid #e8ddc8;">\' +
                f\'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">\' +
                f\'<div style="display:flex;gap:8px;align-items:center;">\' +
                f\'<span style="font-size:10px;font-weight:700;color:#3D2B1F;">{row["unidade_curta"]}</span>\' +
                f\'<span style="font-size:9px;background:#e8ddc8;color:#3D2B1F;padding:2px 6px;border-radius:4px;">{tema_badge}</span>\' +
                (f\'<span style="font-size:9px;background:#f5e8e8;color:#8B2E2E;padding:2px 6px;border-radius:4px;">{subtema_badge}</span>\' if subtema_badge else "") +
                f\'</div>\' +
                f\'<div style="display:flex;gap:8px;align-items:center;">\' +
                f\'<span style="font-size:11px;color:{cor_nota_v};font-weight:700;">{estrelas}</span>\' +
                f\'<span style="font-size:10px;color:#8B7A5A;">{canal_icon} {str(row["data"])[:10]}</span>\' +
                f\'</div></div>\' +
                f\'<div style="font-size:12px;color:#3D2B1F;line-height:1.5;">{str(row["comentario"])[:300]}{"..." if len(str(row["comentario"])) > 300 else ""}</div></div>\',
                unsafe_allow_html=True)

'''

lines[302:616] = [novo]
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print(f'OK — {len(lines)} linhas')
