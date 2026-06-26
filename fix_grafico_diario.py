content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''        with st.container(border=True):
            st.markdown(\'<div class="section-title">Vendas por Dia da Semana</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Distribuicao estimada do faturamento por dia da semana no periodo selecionado.</div>\', unsafe_allow_html=True)
            # Usar periodo mais recente (mes corrente) — ordenar por data
            from datetime import datetime as _dt
            def _parse_per(p):
                try: return _dt.strptime(p.split("-")[1].strip(), "%d/%m/%Y")
                except: return _dt(2000,1,1)
            periodo_mes_atual = max(periodos, key=_parse_per) if periodos else periodo_sel_v
            df_dias_v = df_ifood_dias[df_ifood_dias["periodo"] == periodo_mes_atual].copy()
            if len(df_dias_v) > 0:
                ordem_dias = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]
                df_dias_v["dia_norm"] = df_dias_v["dia_semana"].str.normalize("NFKD").str.encode("ascii","ignore").str.decode("ascii").str.strip()
                dias_g = df_dias_v.groupby("dia_norm")["pedidos"].sum().reset_index()
                fat_total_per = df_v[df_v["periodo"]==periodo_mes_atual]["faturamento"].sum()
                ped_total_per = dias_g["pedidos"].sum()
                dias_g["fat_est"] = dias_g["pedidos"] / ped_total_per * fat_total_per if ped_total_per > 0 else 0
                dias_g = dias_g.set_index("dia_norm").reindex([d for d in ordem_dias if d in dias_g.index]).reset_index()
                fig_dias_fat = go.Figure(go.Bar(
                    x=dias_g["dia_norm"],
                    y=dias_g["fat_est"],
                    marker_color=["#B8923A" if d in ["Sabado","Domingo"] else VERDE for d in dias_g["dia_norm"]],
                    text=dias_g["fat_est"].apply(lambda v: f"R$ {v:,.0f}".replace(",",".")),
                    textposition="outside",
                    textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_dias_fat.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM), showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM), tickprefix="R$ "),
                    font=dict(family="Nunito"), height=300
                )
                st.plotly_chart(fig_dias_fat, use_container_width=True, key="fig_dias_fat_ifood")
                st.markdown(\'<div style="font-size:10px;color:#8B7A5A;margin-top:4px;">* Faturamento estimado proporcionalmente ao volume de pedidos por dia.</div>\', unsafe_allow_html=True)
            else:
                st.info("Sem dados de dias para o periodo selecionado.")'''

new = '''        with st.container(border=True):
            st.markdown(\'<div class="section-title">Vendas Diarias — Mes Corrente</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Faturamento iFood por dia do mes corrente. Atualizado diariamente.</div>\', unsafe_allow_html=True)
            if len(df_ifood_diario) > 0:
                df_id = df_ifood_diario.copy()
                df_id["data"] = pd.to_datetime(df_id["data"])
                _hoje_id = df_id["data"].max()
                df_id_mes = df_id[(df_id["data"].dt.month == _hoje_id.month) & (df_id["data"].dt.year == _hoje_id.year)]
                df_id_rede = df_id_mes.groupby("data").agg(faturamento=("faturamento","sum"), pedidos=("pedidos","sum")).reset_index().sort_values("data")
                fig_diario = go.Figure()
                fig_diario.add_trace(go.Bar(
                    x=df_id_rede["data"].dt.strftime("%d/%m"),
                    y=df_id_rede["faturamento"],
                    marker_color=VERDE,
                    text=df_id_rede["faturamento"].apply(lambda v: f"R$ {v:,.0f}".replace(",",".")),
                    textposition="outside",
                    textfont=dict(family="Nunito", size=9, color=MARROM)
                ))
                fat_acum = df_id_rede["faturamento"].sum()
                fig_diario.add_hline(
                    y=df_id_rede["faturamento"].mean(),
                    line_dash="dot", line_color="#B8923A",
                    annotation_text=f"Media: R$ {df_id_rede['faturamento'].mean():,.0f}".replace(',','.'),
                    annotation_font=dict(size=10, color="#B8923A")
                )
                fig_diario.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM), showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM), tickprefix="R$ "),
                    font=dict(family="Nunito"), height=300
                )
                st.plotly_chart(fig_diario, use_container_width=True, key="fig_diario_ifood")
                col_d1, col_d2, col_d3 = st.columns(3)
                with col_d1: st.metric("MTD Diario", f"R$ {fat_acum:,.0f}".replace(",","."))
                with col_d2: st.metric("Dias com dados", len(df_id_rede))
                with col_d3: st.metric("Media/dia", f"R$ {df_id_rede['faturamento'].mean():,.0f}".replace(",","."))
            else:
                st.info("Sem dados diarios. Rode importar_ifood_diario.py apos subir o arquivo em data/ifood_diario/.")'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
