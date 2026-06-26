content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '        st.markdown("<br>", unsafe_allow_html=True)\n        col_h1, col_h2 = st.columns(2)\n        with col_h1:\n            with st.container(border=True):\n                st.markdown(\'<div class="section-title">Horario de Pico</div>\''

new = '''        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(\'<div class="section-title">Share iFood na Receita Total (Salao + iFood)</div>\', unsafe_allow_html=True)
            st.markdown(\'<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">% do faturamento total representado pelo iFood a cada mes.</div>\', unsafe_allow_html=True)
            share_data = []
            df_vd_share = df_vendas_diarias.copy()
            df_vd_share["data"] = pd.to_datetime(df_vd_share["data"])
            df_vd_share["mes_ano"] = df_vd_share["data"].dt.strftime("%m/%Y")
            venda_salao_mes = df_vd_share.groupby("mes_ano")["venda_salao"].sum().reset_index()
            venda_salao_mes.columns = ["mes_ano", "salao"]
            mes_map_share = {"01":"Jan","02":"Fev","03":"Mar","04":"Abr","05":"Mai","06":"Jun","07":"Jul","08":"Ago","09":"Set","10":"Out","11":"Nov","12":"Dez"}
            for p in periodos:
                try:
                    partes = p.split("-")
                    d_ini = datetime.strptime(partes[0].strip(), "%d/%m/%Y")
                    mes_ano_key = f"{d_ini.month:02d}/{d_ini.year}"
                    fat_if_p = df_v[df_v["periodo"] == p]["faturamento"].sum()
                    salao_p = venda_salao_mes[venda_salao_mes["mes_ano"] == mes_ano_key]["salao"].sum()
                    total_p = salao_p + fat_if_p
                    share_p = fat_if_p / total_p * 100 if total_p > 0 else 0
                    mes_label_s = mes_map_share.get(f"{d_ini.month:02d}", p[:3])
                    share_data.append({"mes": mes_label_s, "share": share_p, "fat_if": fat_if_p, "salao": salao_p, "total": total_p})
                except:
                    pass
            if len(share_data) > 0:
                fig_share = go.Figure()
                meses_s = [s["mes"] for s in share_data]
                shares_s = [s["share"] for s in share_data]
                fig_share.add_trace(go.Scatter(
                    x=meses_s, y=shares_s,
                    mode="lines+markers+text",
                    name="Share iFood",
                    line=dict(color="#4A90D9", width=3),
                    marker=dict(size=10, color="#4A90D9"),
                    text=[f"{v:.1f}%" for v in shares_s],
                    textposition="top center",
                    textfont=dict(family="Nunito", size=11, color="#4A90D9"),
                    hovertemplate="<b>%{x}</b><br>Share: %{y:.1f}%<br><extra></extra>"
                ))
                fig_share.add_hline(
                    y=sum(shares_s)/len(shares_s),
                    line_dash="dot", line_color="#B8923A",
                    annotation_text=f"Media: {sum(shares_s)/len(shares_s):.1f}%",
                    annotation_font=dict(size=10, color="#B8923A")
                )
                fig_share.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=30,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=12, color=MARROM), showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=11, color=MARROM), ticksuffix="%"),
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM)),
                    font=dict(family="Nunito"), height=300
                )
                st.plotly_chart(fig_share, use_container_width=True, key="fig_share_ifood")

        st.markdown("<br>", unsafe_allow_html=True)
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            with st.container(border=True):
                st.markdown(\'<div class="section-title">Horario de Pico</div>\''''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
