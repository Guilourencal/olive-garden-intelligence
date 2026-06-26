content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '\nelif aba_sel == "Social":\n    df_social_f = df_social.copy()'

new = '''
    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 6 — REPUTACAO DIGITAL
    with st.container(border=True):
        st.markdown(\'<div class="section-title">Reputacao Digital — iFood, Google e TripAdvisor</div>\', unsafe_allow_html=True)
        st.markdown(\'<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Reviews coletados das plataformas digitais — complemento às reclamacoes do Buzzmonitor.</div>\', unsafe_allow_html=True)

        df_rev = df_reviews.copy()
        df_rev = df_rev[df_rev["sentimento"].notna()]

        # KPIs por plataforma
        col_p1, col_p2, col_p3 = st.columns(3)
        plataformas = [("iFood","#B8923A"),("Google Reviews","#4A90D9"),("TripAdvisor","#2e6b3e")]
        for col_p, (plat, cor) in zip([col_p1,col_p2,col_p3], plataformas):
            df_plat = df_rev[df_rev["plataforma"]==plat]
            n = len(df_plat)
            nota = df_plat["nota"].mean() if df_plat["nota"].notna().any() else 0
            pct_pos = len(df_plat[df_plat["sentimento"]=="Positivo"]) / n * 100 if n > 0 else 0
            with col_p:
                with st.container(border=True):
                    st.markdown(
                        f\'<div style="text-align:center;padding:8px;">\' +
                        f\'<div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:6px;">{plat.upper()}</div>\' +
                        f\'<div style="font-size:28px;font-weight:800;color:{cor};">{"★"*int(round(nota))}</div>\' +
                        f\'<div style="font-size:20px;font-weight:700;color:{cor};">{nota:.1f}</div>\' +
                        f\'<div style="font-size:10px;color:#8B7A5A;">{n} reviews | {pct_pos:.0f}% positivos</div></div>\',
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Distribuicao de notas
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Distribuicao de Notas por Plataforma</div>\', unsafe_allow_html=True)
            fig_notas = go.Figure()
            for plat, cor in plataformas:
                df_plat = df_rev[df_rev["plataforma"]==plat]
                dist = df_plat["nota"].dropna().value_counts().sort_index()
                fig_notas.add_trace(go.Bar(
                    x=[str(int(n))+"★" for n in dist.index],
                    y=dist.values,
                    name=plat,
                    marker_color=cor
                ))
            fig_notas.update_layout(
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=10),
                xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM), showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                font=dict(family="Nunito"), height=260
            )
            st.plotly_chart(fig_notas, use_container_width=True, key="fig_notas_rev")
        with col_d2:
            st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Sentimento por Plataforma</div>\', unsafe_allow_html=True)
            sent_data = []
            for plat, cor in plataformas:
                df_plat = df_rev[df_rev["plataforma"]==plat]
                for sent in ["Positivo","Neutro","Negativo"]:
                    n_sent = len(df_plat[df_plat["sentimento"]==sent])
                    sent_data.append({"plataforma":plat,"sentimento":sent,"n":n_sent})
            df_sent = pd.DataFrame(sent_data)
            cores_sent = {"Positivo":"#2e6b3e","Neutro":"#B8923A","Negativo":VERMELHO}
            fig_sent = go.Figure()
            for sent in ["Positivo","Neutro","Negativo"]:
                df_s = df_sent[df_sent["sentimento"]==sent]
                fig_sent.add_trace(go.Bar(
                    x=df_s["plataforma"], y=df_s["n"],
                    name=sent, marker_color=cores_sent[sent]
                ))
            fig_sent.update_layout(
                barmode="stack",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=10),
                xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM), showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                font=dict(family="Nunito"), height=260
            )
            st.plotly_chart(fig_sent, use_container_width=True, key="fig_sent_rev")

        st.markdown("<br>", unsafe_allow_html=True)

        # Filtros reviews
        col_rf1, col_rf2, col_rf3 = st.columns(3)
        with col_rf1:
            plat_sel_rev = st.selectbox("Plataforma:", ["Todas","iFood","Google Reviews","TripAdvisor"], key="rev_plat")
        with col_rf2:
            sent_sel_rev = st.selectbox("Sentimento:", ["Todos","Positivo","Neutro","Negativo"], key="rev_sent")
        with col_rf3:
            fil_sel_rev = st.selectbox("Filial:", ["Todas"] + sorted(df_rev["filial"].dropna().unique().tolist()), key="rev_fil")

        df_rev_f = df_rev.copy()
        if plat_sel_rev != "Todas":
            df_rev_f = df_rev_f[df_rev_f["plataforma"]==plat_sel_rev]
        if sent_sel_rev != "Todos":
            df_rev_f = df_rev_f[df_rev_f["sentimento"]==sent_sel_rev]
        if fil_sel_rev != "Todas":
            df_rev_f = df_rev_f[df_rev_f["filial"]==fil_sel_rev]

        st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin:12px 0 8px 0;">Reviews Recentes</div>\', unsafe_allow_html=True)
        for _, row in df_rev_f.head(30).iterrows():
            nota_r = row["nota"]
            cor_r = "#2e6b3e" if pd.notna(nota_r) and nota_r >= 4 else "#B8923A" if pd.notna(nota_r) and nota_r >= 3 else VERMELHO
            estrelas_r = "★" * int(nota_r) if pd.notna(nota_r) else "—"
            filial_r = str(row["filial"]).replace("Olive Garden - ","") if pd.notna(row["filial"]) else "—"
            texto_r = str(row.get("texto","")) if pd.notna(row.get("texto","")) else "—"
            st.markdown(
                f\'<div style="padding:10px 0;border-bottom:1px solid #e8ddc8;">\' +
                f\'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">\' +
                f\'<div style="display:flex;gap:8px;align-items:center;">\' +
                f\'<span style="font-size:10px;font-weight:700;color:#3D2B1F;">{filial_r}</span>\' +
                f\'<span style="font-size:9px;background:#e8ddc8;color:#3D2B1F;padding:2px 6px;border-radius:4px;">{row["plataforma"]}</span>\' +
                f\'</div>\' +
                f\'<span style="font-size:12px;color:{cor_r};font-weight:700;">{estrelas_r}</span></div>\' +
                f\'<div style="font-size:12px;color:#3D2B1F;line-height:1.5;">{texto_r[:250]}{"..." if len(texto_r)>250 else ""}</div></div>\',
                unsafe_allow_html=True)

elif aba_sel == "Social":
    df_social_f = df_social.copy()'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
