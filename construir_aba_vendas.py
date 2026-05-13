# Script seguro para adicionar aba Vendas
lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')

# 1. Encontrar onde inserir as funcoes (apos carregar_pesquisa_performance)
insert_func = None
for i, line in enumerate(lines):
    if 'def carregar_pesquisa_performance():' in line:
        insert_func = i + 5
        break

if not insert_func:
    print('ERRO: nao encontrou carregar_pesquisa_performance')
    exit()

# 2. Inserir funcoes iFood
funcoes = [
    '',
    '@st.cache_data(ttl=300)',
    'def carregar_ifood_vendas():',
    '    conn = get_conn()',
    '    df = pd.read_sql("SELECT * FROM ifood_vendas ORDER BY periodo, filial", conn)',
    '    conn.close()',
    '    return df',
    '',
    '@st.cache_data(ttl=300)',
    'def carregar_ifood_horarios():',
    '    conn = get_conn()',
    '    df = pd.read_sql("SELECT * FROM ifood_horarios", conn)',
    '    conn.close()',
    '    return df',
    '',
    '@st.cache_data(ttl=300)',
    'def carregar_ifood_pagamentos():',
    '    conn = get_conn()',
    '    df = pd.read_sql("SELECT * FROM ifood_pagamentos", conn)',
    '    conn.close()',
    '    return df',
    '',
    '@st.cache_data(ttl=300)',
    'def carregar_ifood_dias():',
    '    conn = get_conn()',
    '    df = pd.read_sql("SELECT * FROM ifood_dias", conn)',
    '    conn.close()',
    '    return df',
]
lines = lines[:insert_func] + funcoes + lines[insert_func:]
print(f'Funcoes inseridas apos linha {insert_func}')

# 3. Encontrar chamadas e inserir calls iFood
for i, line in enumerate(lines):
    if 'df_perf = carregar_pesquisa_performance()' in line:
        insert_call = i + 1
        break

calls = [
    'df_ifood_vendas = carregar_ifood_vendas()',
    'df_ifood_horarios = carregar_ifood_horarios()',
    'df_ifood_pagamentos = carregar_ifood_pagamentos()',
    'df_ifood_dias = carregar_ifood_dias()',
]
lines = lines[:insert_call] + calls + lines[insert_call:]
print(f'Calls inseridas apos linha {insert_call}')

# 4. Adicionar Vendas no sidebar
for i, line in enumerate(lines):
    if 'for aba in' in line and 'OlivIA' in line and 'Vendas' not in line:
        lines[i] = '    for aba in ["Reviews", "Social", "Pesquisa", "Correlacoes", "Vendas", "OlivIA"]:'
        print(f'Sidebar atualizado na linha {i+1}')
        break

# 5. Encontrar linha da aba OlivIA para inserir Vendas antes
olivia_line = None
for i, line in enumerate(lines):
    if line.strip().startswith('elif aba_sel ==') and 'OlivIA' in line:
        olivia_line = i
        break

print(f'OlivIA encontrada na linha {olivia_line+1}')

# 6. Construir conteudo da aba Vendas
aba_vendas = [
    'elif aba_sel == "Vendas":',
    '    st.markdown(\'\'\'<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Vendas</div>',
    '    <div style="font-size:13px; color:#8B9A2E; letter-spacing:0.1em; margin-bottom:20px;">PERFORMANCE FINANCEIRA — iFOOD</div>\'\'\', unsafe_allow_html=True)',
    '',
    '    df_v = df_ifood_vendas[df_ifood_vendas["logistica"] == "Entrega parceira"].copy()',
    '    df_v["filial_curta"] = df_v["filial"].str.replace("Olive Garden - ", "", regex=False)',
    '    periodos = sorted(df_v["periodo"].unique())',
    '',
    '    # Cards executivos',
    '    with st.container(border=True):',
    '        st.markdown(\'<div class="section-title">Visao Executiva</div>\', unsafe_allow_html=True)',
    '        cols_v = st.columns(len(periodos))',
    '        prev_fat = None',
    '        for idx, periodo in enumerate(periodos):',
    '            df_per = df_v[df_v["periodo"] == periodo]',
    '            fat = df_per["faturamento"].sum()',
    '            ped = int(df_per["pedidos"].sum())',
    '            tkt = fat / ped if ped > 0 else 0',
    '            nov = int(df_per["novos_clientes"].sum())',
    '            mes = periodo.split("/")[1].strip()[:2] if "/" in periodo else periodo[:3]',
    '            mes_map = {"01":"Jan","02":"Fev","03":"Mar","04":"Abr","05":"Mai","06":"Jun","07":"Jul","08":"Ago","09":"Set","10":"Out","11":"Nov","12":"Dez"}',
    '            mes_label = mes_map.get(mes, periodo)',
    '            delta_txt = f" (+{((fat/prev_fat-1)*100):.1f}%)" if prev_fat and prev_fat > 0 else ""',
    '            prev_fat = fat',
    '            fat_fmt = f"R$ {fat:,.0f}".replace(",", ".")',
    '            tkt_fmt = f"R$ {tkt:.0f}"',
    '            with cols_v[idx]:',
    '                st.markdown(f\'\'\'<div style="background:#3D2B1F; border-radius:12px; padding:20px; color:#F5F0E8; margin-bottom:8px;">',
    '                    <div style="font-size:10px; letter-spacing:3px; color:#8B9A2E; text-transform:uppercase; margin-bottom:14px;">{mes_label}{delta_txt}</div>',
    '                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">',
    '                    <div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">FATURAMENTO</div>',
    '                    <div style="font-size:16px; font-weight:700;">{fat_fmt}</div></div>',
    '                    <div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">PEDIDOS</div>',
    '                    <div style="font-size:16px; font-weight:700;">{ped:,}</div></div>',
    '                    <div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">TICKET MEDIO</div>',
    '                    <div style="font-size:16px; font-weight:700; color:#8B9A2E;">{tkt_fmt}</div></div>',
    '                    <div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">NOVOS CLIENTES</div>',
    '                    <div style="font-size:16px; font-weight:700; color:#8B9A2E;">{nov:,}</div></div>',
    '                    </div></div>\'\'\', unsafe_allow_html=True)',
    '',
    '    st.markdown("<br>", unsafe_allow_html=True)',
    '',
    '    periodo_sel_v = st.selectbox("Periodo:", periodos, index=len(periodos)-1, key="periodo_v")',
    '    df_vp = df_v[df_v["periodo"] == periodo_sel_v]',
    '',
    '    # Ranking por filial',
    '    with st.container(border=True):',
    '        st.markdown(\'<div class="section-title">Faturamento por Filial</div>\', unsafe_allow_html=True)',
    '        df_rank = df_vp.groupby("filial_curta").agg(faturamento=("faturamento","sum"), pedidos=("pedidos","sum"), novos_clientes=("novos_clientes","sum")).reset_index()',
    '        df_rank["ticket_medio"] = (df_rank["faturamento"] / df_rank["pedidos"]).round(0)',
    '        df_rank = df_rank.sort_values("faturamento", ascending=True)',
    '        df_rank["fat_fmt"] = df_rank["faturamento"].apply(lambda v: f"R$ {v:,.0f}".replace(",","."))',
    '        fig_rank = go.Figure()',
    '        fig_rank.add_trace(go.Bar(',
    '            y=df_rank["filial_curta"],',
    '            x=df_rank["faturamento"],',
    '            orientation="h",',
    '            marker_color=VERDE,',
    '            text=df_rank["fat_fmt"],',
    '            textposition="outside",',
    '            textfont=dict(family="Nunito", size=12, color=MARROM),',
    '        ))',
    '        fig_rank.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=150), xaxis=dict(showgrid=False, tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(tickfont=dict(family="Nunito", size=12, color=MARROM)), font=dict(family="Nunito"), height=280)',
    '        st.plotly_chart(fig_rank, use_container_width=True, key="fig_rank_v")',
    '',
    '    st.markdown("<br>", unsafe_allow_html=True)',
    '',
    '    col_h1, col_h2 = st.columns(2)',
    '',
    '    with col_h1:',
    '        with st.container(border=True):',
    '            st.markdown(\'<div class="section-title">Horario de Pico</div>\', unsafe_allow_html=True)',
    '            df_hor = df_ifood_horarios[df_ifood_horarios["periodo"] == periodo_sel_v].groupby(["periodo_semana","horario"])["pedidos"].sum().reset_index()',
    '            if len(df_hor) > 0:',
    '                df_hor_piv = df_hor.pivot(index="horario", columns="periodo_semana", values="pedidos").fillna(0)',
    '                fig_hor = go.Figure(data=go.Heatmap(z=df_hor_piv.values, x=df_hor_piv.columns.tolist(), y=df_hor_piv.index.tolist(), colorscale=[[0,"#F5F0E8"],[0.5,"#B8923A"],[1,VERDE]], texttemplate="%{z:.0f}", textfont=dict(family="Nunito", size=11)))',
    '                fig_hor.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10), xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"), height=380, coloraxis_showscale=False)',
    '                st.plotly_chart(fig_hor, use_container_width=True, key="fig_hor_v")',
    '',
    '    with col_h2:',
    '        with st.container(border=True):',
    '            st.markdown(\'<div class="section-title">Dias de Pico</div>\', unsafe_allow_html=True)',
    '            ordem_dias = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]',
    '            df_dias = df_ifood_dias[df_ifood_dias["periodo"] == periodo_sel_v].copy()',
    '            df_dias["dia_norm"] = df_dias["dia_semana"].str.normalize("NFKD").str.encode("ascii","ignore").str.decode("ascii").str.strip()',
    '            df_dias_g = df_dias.groupby("dia_norm")["pedidos"].sum().reset_index()',
    '            df_dias_ord = [d for d in ordem_dias if d in df_dias_g["dia_norm"].values]',
    '            df_dias_g = df_dias_g.set_index("dia_norm").reindex(df_dias_ord).reset_index()',
    '            if len(df_dias_g) > 0:',
    '                fig_dias = go.Figure(go.Bar(x=df_dias_g["dia_norm"], y=df_dias_g["pedidos"], marker_color=VERDE, text=df_dias_g["pedidos"], textposition="outside", textfont=dict(family="Nunito", size=12, color=MARROM)))',
    '                fig_dias.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10), xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(showgrid=False, tickfont=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"), height=380)',
    '                st.plotly_chart(fig_dias, use_container_width=True, key="fig_dias_v")',
    '',
    '    st.markdown("<br>", unsafe_allow_html=True)',
    '',
    '    with st.container(border=True):',
    '        st.markdown(\'<div class="section-title">Mix de Pagamento</div>\', unsafe_allow_html=True)',
    '        df_pag = df_ifood_pagamentos[df_ifood_pagamentos["periodo"] == periodo_sel_v].groupby("forma_pagamento")["pedidos"].sum().reset_index().sort_values("pedidos", ascending=False)',
    '        if len(df_pag) > 0:',
    '            fig_pag = go.Figure(go.Pie(labels=df_pag["forma_pagamento"], values=df_pag["pedidos"], hole=0.5, textinfo="label+percent", textfont=dict(family="Nunito", size=12), marker=dict(colors=[VERDE,"#B8923A","#3D7A5C","#7A3D3D","#3D5A7A","#7A5C3D","#5C7A3D","#7A6B3D"])))',
    '            fig_pag.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10), legend=dict(font=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"), height=320)',
    '            st.plotly_chart(fig_pag, use_container_width=True, key="fig_pag_v")',
    '',
]

lines = lines[:olivia_line] + aba_vendas + lines[olivia_line:]
print(f'Aba Vendas inserida antes da linha {olivia_line+1}')

open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('Arquivo salvo!')
