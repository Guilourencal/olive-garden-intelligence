content = open('dashboard.py', 'r', encoding='utf-8').read()

old = 'st.markdown(\n    \'<div style="text-align:center; font-size:10px; color:#B8A898; letter-spacing:0.1em; padding-top:20px;">'

new = '''elif aba_sel == "Fila":
    st.markdown(\'<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Fila de Espera</div>\', unsafe_allow_html=True)

    if len(df_fila) == 0:
        st.warning("Sem dados de fila. Rode importar_fila_espera.py.")
    else:
        df_fe = df_fila.copy()
        df_fe["dia_chegada"] = pd.to_datetime(df_fe["dia_chegada"])
        df_fe["dow"] = df_fe["dia_chegada"].dt.dayofweek
        df_fe["mes"] = df_fe["dia_chegada"].dt.to_period("M").astype(str)
        df_fe["hora_num"] = df_fe["hora_chegada"].apply(lambda x: int(str(x)[:2]) if pd.notna(x) else None)
        df_fe["turno"] = df_fe["hora_num"].apply(lambda h: "Almoco" if h and 11<=h<=15 else "Jantar" if h and 16<=h<=22 else "Outros")
        dias_label = {0:"Seg",1:"Ter",2:"Qua",3:"Qui",4:"Sex",5:"Sab",6:"Dom"}

        # Filtros
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            meses_disp = ["Todos"] + sorted(df_fe["mes"].unique().tolist())
            mes_sel_f = st.selectbox("Mes:", meses_disp, key="fila_mes")
        with col_f2:
            status_disp = ["Todos"] + sorted(df_fe["status"].dropna().unique().tolist())
            status_sel_f = st.selectbox("Status:", status_disp, key="fila_status")
        with col_f3:
            unid_disp = ["Todas"] + sorted(df_fe["unidade"].dropna().unique().tolist()) if df_fe["unidade"].notna().any() else ["Todas"]
            unid_sel_f = st.selectbox("Unidade:", unid_disp, key="fila_unidade")

        df_ff = df_fe.copy()
        if mes_sel_f != "Todos":
            df_ff = df_ff[df_ff["mes"] == mes_sel_f]
        if status_sel_f != "Todos":
            df_ff = df_ff[df_ff["status"] == status_sel_f]
        if unid_sel_f != "Todas":
            df_ff = df_ff[df_ff["unidade"] == unid_sel_f]

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 1 — KPIs
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Resumo Executivo</div>\', unsafe_allow_html=True)
            total = len(df_ff)
            sentados = len(df_ff[df_ff["status"]=="Sentado"])
            cancelados = len(df_ff[df_ff["status"].str.contains("Cancelado", na=False)])
            noshow = len(df_ff[df_ff["status"].str.contains("no-show", case=False, na=False)])
            tx_conv = sentados/total*100 if total>0 else 0
            espera_media = df_ff[df_ff["status"]=="Sentado"]["duracao_minutos"].mean()
            grupo_medio = df_ff["pessoas"].mean()
            col_k1,col_k2,col_k3,col_k4,col_k5,col_k6 = st.columns(6)
            with col_k1: st.metric("Total Filas", total)
            with col_k2:
                cor_conv = "#2e6b3e" if tx_conv>=80 else "#B8923A" if tx_conv>=60 else VERMELHO
                st.markdown(f\'<div style="text-align:center;"><div style="font-size:12px;color:#8B7A5A;">Taxa Conversao</div><div style="font-size:24px;font-weight:700;color:{cor_conv};">{tx_conv:.1f}%</div></div>\', unsafe_allow_html=True)
            with col_k3: st.metric("Sentados", sentados)
            with col_k4: st.metric("Cancelamentos", cancelados)
            with col_k5: st.metric("No-show", noshow)
            with col_k6:
                cor_esp = "#2e6b3e" if pd.notna(espera_media) and espera_media<=15 else "#B8923A" if pd.notna(espera_media) and espera_media<=30 else VERMELHO
                st.markdown(f\'<div style="text-align:center;"><div style="font-size:12px;color:#8B7A5A;">Espera Media</div><div style="font-size:24px;font-weight:700;color:{cor_esp};">{espera_media:.0f} min</div></div>\' if pd.notna(espera_media) else \'<div style="text-align:center;"><div style="font-size:12px;color:#8B7A5A;">Espera Media</div><div style="font-size:24px;font-weight:700;color:#8B7A5A;">—</div></div>\', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 2 — CONVERSAO E ESPERA
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Conversao e Tempo de Espera</div>\', unsafe_allow_html=True)
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Status da Fila</div>\', unsafe_allow_html=True)
                status_cnt = df_ff["status"].value_counts().reset_index()
                status_cnt.columns = ["status","n"]
                cores_status = {"Sentado":"#2e6b3e","Cancelado por solicitação do cliente":"#B8923A","Cancelado pelo cliente":VERMELHO,"Cancelado por no-show do cliente":"#8B7A5A"}
                fig_status = go.Figure(go.Pie(
                    labels=status_cnt["status"], values=status_cnt["n"],
                    marker_colors=[cores_status.get(s, MARROM) for s in status_cnt["status"]],
                    hole=0.4, textfont=dict(family="Nunito", size=11)
                ))
                fig_status.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10),
                    legend=dict(font=dict(family="Nunito", size=9, color=MARROM)), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_status, use_container_width=True, key="fig_status_fila")
            with col_c2:
                st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Distribuicao do Tempo de Espera (Sentados)</div>\', unsafe_allow_html=True)
                df_sent = df_ff[df_ff["status"]=="Sentado"]["duracao_minutos"].dropna()
                fig_hist = go.Figure(go.Histogram(
                    x=df_sent, nbinsx=20,
                    marker_color=VERDE, opacity=0.8
                ))
                fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(title="Minutos", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10)),
                    font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_hist, use_container_width=True, key="fig_hist_fila")

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 3 — HEATMAP HORA x DIA
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Heatmap — Volume de Filas por Hora e Dia</div>\', unsafe_allow_html=True)
            df_heat = df_ff.dropna(subset=["hora_num","dow"]).copy()
            df_heat["dow_label"] = df_heat["dow"].map(dias_label)
            pivot_heat = df_heat.groupby(["hora_num","dow"]).size().reset_index(name="n")
            if len(pivot_heat) > 0:
                pivot_m = pivot_heat.pivot(index="hora_num", columns="dow", values="n").fillna(0)
                pivot_m.columns = [dias_label.get(c,c) for c in pivot_m.columns]
                fig_heat = go.Figure(data=go.Heatmap(
                    z=pivot_m.values,
                    x=pivot_m.columns.tolist(),
                    y=[f"{h}h" for h in pivot_m.index.tolist()],
                    colorscale=[[0,"#F5F0E8"],[0.5,"#B8923A"],[1,VERDE]],
                    texttemplate="%{z:.0f}",
                    textfont=dict(family="Nunito", size=10)
                ))
                fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    font=dict(family="Nunito"), height=380, coloraxis_showscale=False)
                st.plotly_chart(fig_heat, use_container_width=True, key="fig_heat_fila")

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 4 — ESPERA POR DIA E TURNO
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Tempo Medio de Espera por Dia e Turno</div>\', unsafe_allow_html=True)
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Por Dia da Semana</div>\', unsafe_allow_html=True)
                df_sent2 = df_ff[df_ff["status"]=="Sentado"].copy()
                esp_dow = df_sent2.groupby("dow")["duracao_minutos"].mean().reset_index()
                esp_dow["label"] = esp_dow["dow"].map(dias_label)
                esp_dow = esp_dow.sort_values("dow")
                fig_dow = go.Figure(go.Bar(
                    x=esp_dow["label"], y=esp_dow["duracao_minutos"],
                    marker_color=[VERDE if v<=15 else "#B8923A" if v<=30 else VERMELHO for v in esp_dow["duracao_minutos"]],
                    text=esp_dow["duracao_minutos"].apply(lambda v: f"{v:.0f} min"),
                    textposition="outside", textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_dow.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_dow, use_container_width=True, key="fig_dow_fila")
            with col_d2:
                st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Por Turno</div>\', unsafe_allow_html=True)
                esp_turno = df_sent2.groupby("turno")["duracao_minutos"].agg(["mean","count"]).reset_index()
                esp_turno.columns = ["turno","media","n"]
                fig_turno_f = go.Figure(go.Bar(
                    x=esp_turno["turno"], y=esp_turno["media"],
                    marker_color=[VERDE, "#B8923A", "#8B7A5A"][:len(esp_turno)],
                    text=esp_turno["media"].apply(lambda v: f"{v:.0f} min"),
                    textposition="outside", textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_turno_f.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_turno_f, use_container_width=True, key="fig_turno_fila")

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 5 — TAMANHO DO GRUPO
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Tamanho do Grupo</div>\', unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Distribuicao por Numero de Pessoas</div>\', unsafe_allow_html=True)
                grupo_cnt = df_ff["pessoas"].value_counts().sort_index().reset_index()
                grupo_cnt.columns = ["pessoas","n"]
                fig_grupo = go.Figure(go.Bar(
                    x=grupo_cnt["pessoas"].astype(str)+"p",
                    y=grupo_cnt["n"],
                    marker_color=VERDE,
                    text=grupo_cnt["n"], textposition="outside",
                    textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_grupo.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_grupo, use_container_width=True, key="fig_grupo_fila")
            with col_g2:
                st.markdown(\'<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Espera Media por Tamanho de Grupo</div>\', unsafe_allow_html=True)
                esp_grupo = df_ff[df_ff["status"]=="Sentado"].groupby("pessoas")["duracao_minutos"].mean().reset_index()
                fig_esp_g = go.Figure(go.Scatter(
                    x=esp_grupo["pessoas"], y=esp_grupo["duracao_minutos"],
                    mode="lines+markers+text",
                    line=dict(color=DOURADO, width=2),
                    marker=dict(size=8, color=DOURADO),
                    text=esp_grupo["duracao_minutos"].apply(lambda v: f"{v:.0f}min"),
                    textposition="top center",
                    textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_esp_g.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(title="Pessoas", tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10)),
                    font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_esp_g, use_container_width=True, key="fig_esp_grupo_fila")

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 6 — EVOLUCAO MENSAL
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Evolucao Mensal</div>\', unsafe_allow_html=True)
            evo_mes = df_fe.groupby("mes").agg(
                total=("status","count"),
                sentados=("status", lambda x: (x=="Sentado").sum()),
                espera=("duracao_minutos","mean")
            ).reset_index()
            evo_mes["tx_conv"] = evo_mes["sentados"]/evo_mes["total"]*100
            fig_evo_f = go.Figure()
            fig_evo_f.add_trace(go.Bar(x=evo_mes["mes"], y=evo_mes["total"], name="Total Filas", marker_color="#8B7A5A", opacity=0.6))
            fig_evo_f.add_trace(go.Bar(x=evo_mes["mes"], y=evo_mes["sentados"], name="Sentados", marker_color=VERDE))
            fig_evo_f.add_trace(go.Scatter(x=evo_mes["mes"], y=evo_mes["tx_conv"], name="Taxa Conv. %",
                mode="lines+markers", line=dict(color=DOURADO, width=2), marker=dict(size=8),
                yaxis="y2"))
            fig_evo_f.update_layout(
                barmode="overlay",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=60),
                xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM), showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10)),
                yaxis2=dict(overlaying="y", side="right", ticksuffix="%", showgrid=False, tickfont=dict(family="Nunito", size=10, color=DOURADO)),
                legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                font=dict(family="Nunito"), height=320
            )
            st.plotly_chart(fig_evo_f, use_container_width=True, key="fig_evo_fila")

st.markdown(\n    \'<div style="text-align:center; font-size:10px; color:#B8A898; letter-spacing:0.1em; padding-top:20px;">'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK bloco fila')
else:
    print('TRECHO NAO ENCONTRADO')
