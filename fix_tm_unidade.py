content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''        with col_r2:
            with st.container(border=True):
                st.markdown('<div class="section-title">Ultima Semana Fechada vs Ano Anterior</div>', unsafe_allow_html=True)
                ordem_dias = ["seg","ter","qua","qui","sex","sab","dom"]
                labels_dias = ["Seg","Ter","Qua","Qui","Sex","Sab","Dom"]
                df_dow_base = df_vd.copy()
                if filiais_sel != sorted(df_vd["filial_curta"].unique()):
                    df_dow_base = df_dow_base[df_dow_base["filial_curta"].isin(filiais_sel)]
                df_dow_base["dia_norm"] = df_dow_base["dia_semana"].str[:3].str.lower()
                # Ultima semana fechada
                hoje = df_dow_base["data"].max()
                semanas = df_dow_base["semana"].dropna().unique()
                # Ultima semana fechada (seg a dom)
                from datetime import timedelta
                df_dow_base["data_dt"] = pd.to_datetime(df_dow_base["data"])
                hoje_dt = df_dow_base["data_dt"].max()
                # Encontrar o ultimo domingo fechado
                dias_desde_dom = (hoje_dt.weekday() + 1) % 7
                ultimo_dom = hoje_dt - timedelta(days=dias_desde_dom)
                ultima_seg = ultimo_dom - timedelta(days=6)
                df_ult = df_dow_base[(df_dow_base["data_dt"] >= ultima_seg) & (df_dow_base["data_dt"] <= ultimo_dom)]
                # Numero da semana ISO da ultima semana fechada
                num_semana = int(ultima_seg.isocalendar()[1])
                ano_atual = int(ultima_seg.year)
                ano_anterior = ano_atual - 1
                # Mesma semana ISO no ano anterior
                df_dow_base["iso_week"] = df_dow_base["data_dt"].dt.isocalendar().week.astype(int)
                df_dow_base["iso_year"] = df_dow_base["data_dt"].dt.isocalendar().year.astype(int)
                df_ano1 = df_dow_base[(df_dow_base["iso_week"] == num_semana) & (df_dow_base["iso_year"] == ano_anterior)]
                sem_label = f"Sem. {num_semana}/{ano_atual} vs Sem. {num_semana}/{ano_anterior}"
                if len(df_ult) > 0:
                    g_ult = df_ult.groupby("dia_norm")["venda_salao"].sum().reset_index()
                    g_ult = g_ult.set_index("dia_norm").reindex([d for d in ordem_dias if d in g_ult["dia_norm"].values]).reset_index()
                    g_ult["label"] = g_ult["dia_norm"].map(dict(zip(ordem_dias, labels_dias)))
                    fig_dow = go.Figure()
                    if len(df_ano1) > 0:
                        g_ano1 = df_ano1.groupby("dia_norm")["venda_salao"].sum().reset_index()
                        g_ano1 = g_ano1.set_index("dia_norm").reindex([d for d in ordem_dias if d in g_ano1["dia_norm"].values]).reset_index()
                        g_ano1["label"] = g_ano1["dia_norm"].map(dict(zip(ordem_dias, labels_dias)))
                        fig_dow.add_trace(go.Bar(x=g_ano1["label"], y=g_ano1["venda_salao"], name=f"Sem. {num_semana}/{ano_anterior}", marker_color="#8B7A5A", opacity=0.6, text=g_ano1["venda_salao"].apply(lambda v: f"R$ {v/1000:.0f}k"), textposition="auto", textfont=dict(family="Nunito", size=9, color="white")))
                    fig_dow.add_trace(go.Bar(x=g_ult["label"], y=g_ult["venda_salao"], name=f"Sem. {num_semana}/{ano_atual}", marker_color=VERDE, text=g_ult["venda_salao"].apply(lambda v: f"R$ {v/1000:.0f}k"), textposition="auto", textfont=dict(family="Nunito", size=9, color="white")))
                    fig_dow.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=30,b=10,l=10,r=10), title=dict(text=f"Semana: {sem_label}", font=dict(family="Nunito", size=10, color="#8B7A5A"), x=0), xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(showgrid=False), legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02), font=dict(family="Nunito"), height=280)
                    st.plotly_chart(fig_dow, use_container_width=True, key="fig_dow_vd")
                else:
                    st.markdown('<div style="padding:20px; text-align:center; color:#8B7A5A;">Sem dados de semana disponíveis</div>', unsafe_allow_html=True)'''

new = '''        with col_r2:
            with st.container(border=True):
                st.markdown('<div class="section-title">Ticket Medio por Unidade</div>', unsafe_allow_html=True)
                st.markdown('<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Media do periodo filtrado acima.</div>', unsafe_allow_html=True)
                df_tm = df_vd_f.groupby("filial_curta").agg(
                    venda=("venda_salao", "sum"),
                    gc=("gc_salao", "sum")
                ).reset_index()
                df_tm["ticket_medio"] = (df_tm["venda"] / df_tm["gc"]).round(2)
                df_tm = df_tm[df_tm["gc"] > 0].sort_values("ticket_medio", ascending=False)
                tm_media = df_tm["ticket_medio"].mean()
                fig_tm = go.Figure(go.Bar(
                    x=df_tm["filial_curta"],
                    y=df_tm["ticket_medio"],
                    marker_color=[VERDE if v >= tm_media else "#B8923A" for v in df_tm["ticket_medio"]],
                    text=df_tm["ticket_medio"].apply(lambda v: f"R$ {v:.2f}"),
                    textposition="outside",
                    textfont=dict(family="Nunito", size=11, color=MARROM)
                ))
                fig_tm.add_hline(y=tm_media, line_dash="dot", line_color="#B8923A",
                    annotation_text=f"Media: R$ {tm_media:.2f}",
                    annotation_font=dict(family="Nunito", size=10, color="#B8923A"))
                fig_tm.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=40),
                    xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)),
                    yaxis=dict(showgrid=False),
                    font=dict(family="Nunito"), height=280
                )
                st.plotly_chart(fig_tm, use_container_width=True, key="fig_tm_vd")'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
