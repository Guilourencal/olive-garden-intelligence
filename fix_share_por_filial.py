content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''            if len(share_data) > 0:
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
                st.plotly_chart(fig_share, use_container_width=True, key="fig_share_ifood")'''

new = '''            if len(share_data) > 0:
                fig_share = go.Figure()
                cores_filial = {
                    "Morumbi": "#B8923A",
                    "Center Norte": "#4A90D9",
                    "Aricanduva": "#2e6b3e",
                    "Dom Pedro": "#c0392b",
                }
                filiais_ifood = [f for f in ["Morumbi","Center Norte","Aricanduva","Dom Pedro"]]
                # Linha por unidade
                for filial_if in filiais_ifood:
                    filial_full = "Olive Garden - " + filial_if
                    share_fil = []
                    for p in periodos:
                        try:
                            partes = p.split("-")
                            d_ini = datetime.strptime(partes[0].strip(), "%d/%m/%Y")
                            mes_ano_key = f"{d_ini.month:02d}/{d_ini.year}"
                            fat_if_fil = df_v[df_v["periodo"]==p][df_v["filial"]==filial_full]["faturamento"].sum() if "filial" in df_v.columns else 0
                            salao_fil = venda_salao_mes[venda_salao_mes["mes_ano"]==mes_ano_key]
                            salao_fil_v = df_vd_share[df_vd_share["mes_ano"]==mes_ano_key & df_vd_share["filial"].str.contains(filial_if)]["venda_salao"].sum() if len(salao_fil)>0 else 0
                            total_fil = salao_fil_v + fat_if_fil
                            share_fil.append(fat_if_fil/total_fil*100 if total_fil>0 else 0)
                        except:
                            share_fil.append(0)
                    meses_s = [s["mes"] for s in share_data]
                    fig_share.add_trace(go.Scatter(
                        x=meses_s, y=share_fil,
                        mode="lines+markers",
                        name=filial_if,
                        line=dict(color=cores_filial.get(filial_if, MARROM), width=2, dash="dot"),
                        marker=dict(size=7, color=cores_filial.get(filial_if, MARROM)),
                        hovertemplate=f"<b>{filial_if}</b><br>%{{x}}: %{{y:.1f}}<extra></extra>"
                    ))
                # Linha rede geral
                meses_s = [s["mes"] for s in share_data]
                shares_s = [s["share"] for s in share_data]
                fig_share.add_trace(go.Scatter(
                    x=meses_s, y=shares_s,
                    mode="lines+markers+text",
                    name="Rede Geral",
                    line=dict(color=VERDE, width=3),
                    marker=dict(size=10, color=VERDE),
                    text=[f"{v:.1f}%" for v in shares_s],
                    textposition="top center",
                    textfont=dict(family="Nunito", size=10, color=VERDE),
                    hovertemplate="<b>Rede</b><br>%{x}: %{y:.1f}%<extra></extra>"
                ))
                fig_share.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=30,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=12, color=MARROM), showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=11, color=MARROM), ticksuffix="%"),
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                    font=dict(family="Nunito"), height=340
                )
                st.plotly_chart(fig_share, use_container_width=True, key="fig_share_ifood")'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
