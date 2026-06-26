content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''        if len(df_perf) > 1:
            df_perf_sm = df_perf[df_perf["restaurant"] != "nan"].copy()
            df_perf_sm["filial_curta"] = df_perf_sm["restaurant"].str.replace("Olive Garden - ", "")
            df_perf_sm["periodo_curto"] = df_perf_sm["periodo"].str.extract(r"(FW\d+ to FW\d+)")
            metricas_sm = ["overall_experience", "value", "service", "taste", "speed_of_service", "clean", "soup_salad_refill", "breadstick_refill"]
            labels_sm = ["Exp. Geral", "Valor", "Atend.", "Sabor", "Velocidade", "Limpeza", "Refil Sopa", "Refil Bread"]
            filiais_sm = sorted(df_perf_sm["filial_curta"].unique())
            cols_sm = st.columns(3)
            for idx, filial in enumerate(filiais_sm):
                df_fil = df_perf_sm[df_perf_sm["filial_curta"] == filial].sort_values("periodo_curto")
                fig_sm = go.Figure()
                for m, lbl in zip(metricas_sm, labels_sm):
                    fig_sm.add_trace(go.Scatter(
                        x=df_fil["periodo_curto"],
                        y=df_fil[m],
                        mode="lines+markers",
                        name=lbl,
                        line=dict(width=1.8),
                        marker=dict(size=6),
                    ))
                fig_sm.update_layout(
                    title=dict(text=filial, font=dict(family="Nunito", size=13, color=MARROM), x=0.5),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=40, b=10, l=10, r=10),
                    legend=dict(font=dict(family="Nunito", size=9, color=MARROM), orientation="h", yanchor="bottom", y=-0.5),
                    xaxis=dict(tickfont=dict(family="Nunito", size=9, color=MARROM)),
                    yaxis=dict(range=[80, 101], showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=9, color=MARROM)),
                    height=280,
                    font=dict(family="Nunito"),
                )
                with cols_sm[idx % 3]:
                    st.plotly_chart(fig_sm, use_container_width=True, key=f"fig_sm_{idx}")'''

new = '''        if len(df_perf) > 1:
            df_perf_sm = df_perf[df_perf["restaurant"] != "nan"].copy()
            df_perf_sm["filial_curta"] = df_perf_sm["restaurant"].str.replace("Olive Garden - ", "")
            df_perf_sm["periodo_curto"] = df_perf_sm["periodo"].str.extract(r"(FW\d+ to FW\d+)")
            df_perf_sm["fw_ini"] = df_perf_sm["periodo_curto"].str.extract(r"FW(\d+)").astype(float)
            metricas_sm = ["overall_experience", "value", "service", "taste", "speed_of_service", "clean", "soup_salad_refill", "breadstick_refill"]
            labels_sm = ["Exp. Geral", "Valor", "Atend.", "Sabor", "Velocidade", "Limpeza", "Refil Sopa", "Refil Bread"]
            cores_sm = ["#3D2B1F","#4A90D9","#B8923A","#2e6b3e","#c0392b","#8B7A5A","#E67E22","#9B59B6"]
            filiais_sm = sorted(df_perf_sm["filial_curta"].unique())
            # Janela deslizante — ultimas 10 semanas
            periodos_disponiveis = sorted(df_perf_sm["periodo_curto"].dropna().unique(), key=lambda p: df_perf_sm[df_perf_sm["periodo_curto"]==p]["fw_ini"].values[0] if len(df_perf_sm[df_perf_sm["periodo_curto"]==p])>0 else 0)
            ultimos_10 = periodos_disponiveis[-10:]
            df_perf_sm = df_perf_sm[df_perf_sm["periodo_curto"].isin(ultimos_10)]
            # Label curto — so FW inicial
            df_perf_sm["label_x"] = df_perf_sm["periodo_curto"].str.extract(r"^(FW\d+)")
            # Layout 3 linhas x 2 colunas
            for row_idx in range(3):
                cols_sm = st.columns(2)
                for col_idx in range(2):
                    filial_idx = row_idx * 2 + col_idx
                    if filial_idx >= len(filiais_sm):
                        break
                    filial = filiais_sm[filial_idx]
                    df_fil = df_perf_sm[df_perf_sm["filial_curta"] == filial].sort_values("fw_ini")
                    fig_sm = go.Figure()
                    for m, lbl, cor in zip(metricas_sm, labels_sm, cores_sm):
                        fig_sm.add_trace(go.Scatter(
                            x=df_fil["label_x"],
                            y=df_fil[m],
                            mode="lines+markers",
                            name=lbl,
                            line=dict(width=2, color=cor),
                            marker=dict(size=6, color=cor),
                        ))
                    fig_sm.update_layout(
                        title=dict(text=filial, font=dict(family="Nunito", size=13, color=MARROM), x=0.5),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(t=40, b=20, l=10, r=10),
                        legend=dict(font=dict(family="Nunito", size=9, color=MARROM), orientation="h", yanchor="bottom", y=-0.35, x=0),
                        xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM), showgrid=False, tickangle=-30),
                        yaxis=dict(range=[80, 101], showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=9, color=MARROM)),
                        height=320,
                        font=dict(family="Nunito"),
                    )
                    with cols_sm[col_idx]:
                        st.plotly_chart(fig_sm, use_container_width=True, key=f"fig_sm_{filial_idx}")'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
