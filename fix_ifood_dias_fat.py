content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '            st.plotly_chart(fig_evo2, use_container_width=True, key="fig_evo_v2")\n\n        st.markdown("<br>", unsafe_allow_html=True)\n        with st.container(border=True):\n            st.markdown(\'<div class="section-title">Share iFood'

new = '''            st.plotly_chart(fig_evo2, use_container_width=True, key="fig_evo_v2")

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(\'<div class="section-title">Vendas por Dia do Mes</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Faturamento diario no periodo selecionado — identifica picos e vales ao longo do mes.</div>\', unsafe_allow_html=True)
            df_dias_v = df_ifood_dias[df_ifood_dias["periodo"] == periodo_sel_v].copy()
            if len(df_dias_v) > 0:
                ordem_dias = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]
                df_dias_v["dia_norm"] = df_dias_v["dia_semana"].str.normalize("NFKD").str.encode("ascii","ignore").str.decode("ascii").str.strip()
                fat_dia = df_v[df_v["periodo"]==periodo_sel_v].copy()
                # Usar ifood_vendas para pegar faturamento por dia da semana via ifood_dias (pedidos proxy)
                dias_g = df_dias_v.groupby("dia_norm")["pedidos"].sum().reset_index()
                fat_total_per = df_v[df_v["periodo"]==periodo_sel_v]["faturamento"].sum()
                ped_total_per = df_dias_v["pedidos"].sum()
                dias_g["fat_est"] = dias_g["pedidos"] / ped_total_per * fat_total_per if ped_total_per > 0 else 0
                dias_g = dias_g.set_index("dia_norm").reindex([d for d in ordem_dias if d in dias_g["dia_norm"].values]).reset_index()
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
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM),
                               tickprefix="R$ "),
                    font=dict(family="Nunito"), height=300
                )
                st.plotly_chart(fig_dias_fat, use_container_width=True, key="fig_dias_fat_ifood")
                st.markdown(\'<div style="font-size:10px;color:#8B7A5A;margin-top:4px;">* Faturamento estimado proporcionalmente ao volume de pedidos por dia.</div>\', unsafe_allow_html=True)
            else:
                st.info("Sem dados de dias para o periodo selecionado.")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Share iFood'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
