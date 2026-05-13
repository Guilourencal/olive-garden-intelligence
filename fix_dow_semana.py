lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')

novo_dow = [
    '        with col_r2:',
    '            with st.container(border=True):',
    '                st.markdown(\'<div class="section-title">Ultima Semana Fechada vs Ano Anterior</div>\', unsafe_allow_html=True)',
    '                ordem_dias = ["seg","ter","qua","qui","sex","sab","dom"]',
    '                labels_dias = ["Seg","Ter","Qua","Qui","Sex","Sab","Dom"]',
    '                df_dow_base = df_vd.copy()',
    '                if filial_vd_sel != "Todas":',
    '                    df_dow_base = df_dow_base[df_dow_base["filial_curta"] == filial_vd_sel]',
    '                df_dow_base["dia_norm"] = df_dow_base["dia_semana"].str[:3].str.lower()',
    '                # Ultima semana fechada',
    '                hoje = df_dow_base["data"].max()',
    '                semanas = df_dow_base["semana"].dropna().unique()',
    '                ultima_sem = sorted(semanas)[-1] if len(semanas) > 0 else None',
    '                df_ult = df_dow_base[df_dow_base["semana"] == ultima_sem] if ultima_sem else pd.DataFrame()',
    '                # Mesma semana ano anterior',
    '                sem_ano1 = sorted(semanas)[-53] if len(semanas) > 52 else (sorted(semanas)[0] if len(semanas) > 0 else None)',
    '                df_ano1 = df_dow_base[df_dow_base["semana"] == sem_ano1] if sem_ano1 else pd.DataFrame()',
    '                if len(df_ult) > 0:',
    '                    g_ult = df_ult.groupby("dia_norm")["venda_salao"].sum().reset_index()',
    '                    g_ult = g_ult.set_index("dia_norm").reindex([d for d in ordem_dias if d in g_ult["dia_norm"].values]).reset_index()',
    '                    g_ult["label"] = g_ult["dia_norm"].map(dict(zip(ordem_dias, labels_dias)))',
    '                    fig_dow = go.Figure()',
    '                    if len(df_ano1) > 0:',
    '                        g_ano1 = df_ano1.groupby("dia_norm")["venda_salao"].sum().reset_index()',
    '                        g_ano1 = g_ano1.set_index("dia_norm").reindex([d for d in ordem_dias if d in g_ano1["dia_norm"].values]).reset_index()',
    '                        g_ano1["label"] = g_ano1["dia_norm"].map(dict(zip(ordem_dias, labels_dias)))',
    '                        fig_dow.add_trace(go.Bar(x=g_ano1["label"], y=g_ano1["venda_salao"], name="Ano Anterior", marker_color="#8B7A5A", opacity=0.6, text=g_ano1["venda_salao"].apply(lambda v: f"R$ {v/1000:.0f}k"), textposition="outside", textfont=dict(family="Nunito", size=10, color="#8B7A5A")))',
    '                    fig_dow.add_trace(go.Bar(x=g_ult["label"], y=g_ult["venda_salao"], name=f"Semana atual", marker_color=VERDE, text=g_ult["venda_salao"].apply(lambda v: f"R$ {v/1000:.0f}k"), textposition="outside", textfont=dict(family="Nunito", size=10, color=MARROM)))',
    '                    sem_label = str(ultima_sem)[:20] if ultima_sem else ""',
    '                    fig_dow.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=30,b=10,l=10,r=10), title=dict(text=f"Semana: {sem_label}", font=dict(family="Nunito", size=10, color="#8B7A5A"), x=0), xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(showgrid=False), legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02), font=dict(family="Nunito"), height=280)',
    '                    st.plotly_chart(fig_dow, use_container_width=True, key="fig_dow_vd")',
    '                else:',
    '                    st.markdown(\'<div style="padding:20px; text-align:center; color:#8B7A5A;">Sem dados de semana disponíveis</div>\', unsafe_allow_html=True)',
]

result = lines[:1162] + novo_dow + lines[1178:]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result))
print(f'Feito! Total: {len(result)} linhas')
