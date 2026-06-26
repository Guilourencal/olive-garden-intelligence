content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '        st.markdown("<br>", unsafe_allow_html=True)\n\n        # BLOCO 4 — BEBIDAS PUZZLE'
new = '''        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 3b — MATRIZ DE CRUZAMENTO
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Matriz de Cruzamento — Uplift vs Volume</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Eixo X = volume de checks | Eixo Y = Check Uplift (R$) | Tamanho = Impacto Total (Uplift x Checks) | Cor = Tipo Boston</div>\', unsafe_allow_html=True)
            df_matriz = df_mf.copy()
            df_matriz["uplift_calc"] = df_matriz["ct_gross_total_check_avg"] - df_matriz["gross_total_check_avg"]
            df_matriz["impacto_total"] = df_matriz["uplift_calc"] * df_matriz["number_of_checks"]
            df_matriz = df_matriz.dropna(subset=["uplift_calc","number_of_checks","impacto_total"])
            if len(df_matriz) > 0:
                med_up = df_matriz["uplift_calc"].median()
                med_ch = df_matriz["number_of_checks"].median()
                fig_mat = go.Figure()
                for tipo in ["Star","Dog","Puzzle","Horse"]:
                    dft = df_matriz[df_matriz["type"]==tipo]
                    if len(dft) == 0:
                        continue
                    tamanho = dft["impacto_total"].apply(lambda v: max(8, min(50, abs(v)/50000)))
                    fig_mat.add_trace(go.Scatter(
                        x=dft["number_of_checks"],
                        y=dft["uplift_calc"],
                        mode="markers",
                        name=tipo,
                        marker=dict(size=tamanho, color=COR_BOSTON.get(tipo, MARROM), opacity=0.75, line=dict(width=1, color="white")),
                        hovertemplate="<b>%{customdata[0]}</b><br>Checks: %{x}<br>Uplift: R$ %{y:.0f}<br>Impacto: R$ %{customdata[1]:,.0f}<extra></extra>",
                        customdata=list(zip(dft["item"].str[:30], dft["impacto_total"]))
                    ))
                fig_mat.add_vline(x=med_ch, line_dash="dot", line_color="#8B7A5A", line_width=1)
                fig_mat.add_hline(y=med_up, line_dash="dot", line_color="#8B7A5A", line_width=1)
                anotacoes = [
                    dict(x=df_matriz["number_of_checks"].max()*0.85, y=df_matriz["uplift_calc"].max()*0.90, text="Prioridade 1 — Proteger", showarrow=False, font=dict(size=9, color="#2e6b3e")),
                    dict(x=df_matriz["number_of_checks"].min()*1.5, y=df_matriz["uplift_calc"].max()*0.90, text="Promover — Aumentar visibilidade", showarrow=False, font=dict(size=9, color="#4A90D9")),
                    dict(x=df_matriz["number_of_checks"].max()*0.85, y=df_matriz["uplift_calc"].min()*0.90, text="Revisar preco", showarrow=False, font=dict(size=9, color="#B8923A")),
                    dict(x=df_matriz["number_of_checks"].min()*1.5, y=df_matriz["uplift_calc"].min()*0.90, text="Avaliar — Monitorar ou cortar", showarrow=False, font=dict(size=9, color=VERMELHO)),
                ]
                fig_mat.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=40,l=60,r=10),
                    xaxis=dict(title="Numero de Checks", showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                    yaxis=dict(title="Check Uplift (R$)", showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                    annotations=anotacoes,
                    font=dict(family="Nunito"), height=420
                )
                st.plotly_chart(fig_mat, use_container_width=True, key="fig_matriz_menu")
                col_q1, col_q2, col_q3, col_q4 = st.columns(4)
                for col_q, q_label, q_cor, q_desc, q_fn in [
                    (col_q1, "Prioridade 1", "#2e6b3e", "Proteger e impulsionar", lambda r: r["uplift_calc"]>=med_up and r["number_of_checks"]>=med_ch),
                    (col_q2, "Promover", "#4A90D9", "Aumentar visibilidade", lambda r: r["uplift_calc"]>=med_up and r["number_of_checks"]<med_ch),
                    (col_q3, "Revisar preco", "#B8923A", "Avaliar precificacao", lambda r: r["uplift_calc"]<med_up and r["number_of_checks"]>=med_ch),
                    (col_q4, "Avaliar", VERMELHO, "Monitorar ou cortar", lambda r: r["uplift_calc"]<med_up and r["number_of_checks"]<med_ch),
                ]:
                    df_q = df_matriz[df_matriz.apply(q_fn, axis=1)]
                    with col_q:
                        itens_html = "".join([f\'<div style="font-size:10px;color:#3D2B1F;padding:2px 0;border-bottom:1px solid #e8ddc8;">{r["item"][:22]}</div>\' for _, r in df_q.head(5).iterrows()])
                        extra = f\'<div style="font-size:9px;color:#8B7A5A;margin-top:4px;">+{len(df_q)-5} itens</div>\' if len(df_q)>5 else ""
                        st.markdown(
                            f\'<div style="background:#F5F0E8;border-radius:8px;padding:10px;border-left:3px solid {q_cor};">\' +
                            f\'<div style="font-size:10px;font-weight:700;color:{q_cor};margin-bottom:4px;">{q_label}</div>\' +
                            f\'<div style="font-size:9px;color:#8B7A5A;margin-bottom:6px;">{q_desc}</div>\' +
                            itens_html + extra + \'</div>\',
                            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 4 — BEBIDAS PUZZLE'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
