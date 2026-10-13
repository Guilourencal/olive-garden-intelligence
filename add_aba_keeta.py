import pathlib, shutil, datetime

p = pathlib.Path("dashboard.py")
t = p.read_text(encoding="utf-8")

shutil.copy2(p, f"dashboard_backup_keeta_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py")

# 1. Adicionar "Keeta" na lista de abas da sidebar
OLD_ABAS = '["Reviews", "Social", "Pesquisa", "Analises", "Vendas", "OlivIA", "Menu", "Fila"]'
NEW_ABAS = '["Reviews", "Social", "Pesquisa", "Analises", "Vendas", "OlivIA", "Menu", "Fila", "Keeta"]'
assert OLD_ABAS in t, "Lista de abas nao encontrada"
t = t.replace(OLD_ABAS, NEW_ABAS, 1)
print("OK: aba Keeta adicionada na sidebar")

# 2. Encontrar ultimo bloco de aba para inserir apos
ANCHOR = 'if aba_sel == "Fila":'
assert ANCHOR in t, "Ancora nao encontrada"

# Encontrar fim do bloco Fila (proxima linha que nao tem indentacao)
idx = t.index(ANCHOR)
# Inserir bloco Keeta antes do fim do arquivo, apos o bloco Fila
KEETA_BLOCK = '''

# ============================================================
# ABA KEETA
# ============================================================
if aba_sel == "Keeta":
    st.markdown(\'\'\'<div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">
        <span style="font-size:22px;font-weight:700;color:#C8BFB0;letter-spacing:0.05em;">KEETA DELIVERY</span>
        <span style="font-size:11px;color:#8B9A2E;background:rgba(139,154,46,0.12);border:1px solid rgba(139,154,46,0.3);border-radius:4px;padding:2px 8px;">NOVO</span>
    </div>\'\'\', unsafe_allow_html=True)

    import calendar as _cal
    _hoje = __import__("datetime").date.today()
    _mes, _ano = _hoje.month, _hoje.year
    _dias_mes = _cal.monthrange(_ano, _mes)[1]

    with get_conn() as _conn:
        # MTD outubro
        _df_kt = pd.read_sql(f"""
            SELECT data, filial, vendas_itens as gmv, ganhos_liquidos as liquido,
                   comissao, despesa, outras_despesas
            FROM keeta_diario
            WHERE EXTRACT(month FROM data)={_mes} AND EXTRACT(year FROM data)={_ano}
            ORDER BY data
        """, _conn)

        # Historico completo
        _df_hist = pd.read_sql("""
            SELECT data, filial, vendas_itens as gmv, ganhos_liquidos as liquido
            FROM keeta_diario ORDER BY data
        """, _conn)

    if _df_kt.empty:
        st.info("Nenhum dado Keeta importado para este mes.")
    else:
        _tot_gmv  = float(_df_kt["gmv"].sum())
        _tot_liq  = float(_df_kt["liquido"].sum())
        _tot_com  = float(_df_kt["comissao"].sum())
        _tot_desp = float((_df_kt["despesa"] + _df_kt["outras_despesas"]).sum())
        _dias_real = int(_df_kt["data"].nunique())
        _media_liq = _tot_liq / _dias_real if _dias_real > 0 else 0
        _proj_liq  = _tot_liq + _media_liq * (_dias_mes - _dias_real)
        _margem    = _tot_liq / _tot_gmv * 100 if _tot_gmv > 0 else 0

        # KPI row
        _k1, _k2, _k3, _k4 = st.columns(4)
        with _k1:
            st.markdown(f\'\'\'<div style="background:#1e1e1e;border-radius:8px;padding:14px 16px;border-left:3px solid #8B9A2E;">
                <div style="font-size:10px;color:#8B9A2E;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">GMV MTD</div>
                <div style="font-size:20px;font-weight:700;color:#C8BFB0;">R$ {_tot_gmv:,.0f}</div>
                <div style="font-size:10px;color:#8B9A2E;margin-top:3px;">{_dias_real}/{_dias_mes} dias</div>
            </div>\'\'\'.replace(",","."), unsafe_allow_html=True)
        with _k2:
            st.markdown(f\'\'\'<div style="background:#1e1e1e;border-radius:8px;padding:14px 16px;border-left:3px solid #2ECC71;">
                <div style="font-size:10px;color:#8B9A2E;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">LIQUIDO MTD</div>
                <div style="font-size:20px;font-weight:700;color:#2ECC71;">R$ {_tot_liq:,.0f}</div>
                <div style="font-size:10px;color:#8B9A2E;margin-top:3px;">margem {_margem:.1f}%</div>
            </div>\'\'\'.replace(",","."), unsafe_allow_html=True)
        with _k3:
            st.markdown(f\'\'\'<div style="background:#1e1e1e;border-radius:8px;padding:14px 16px;border-left:3px solid #E74C3C;">
                <div style="font-size:10px;color:#8B9A2E;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">COMISSAO + DESP</div>
                <div style="font-size:20px;font-weight:700;color:#E74C3C;">R$ {abs(_tot_com+_tot_desp):,.0f}</div>
                <div style="font-size:10px;color:#8B9A2E;margin-top:3px;">{abs(_tot_com+_tot_desp)/_tot_gmv*100:.1f}% do GMV</div>
            </div>\'\'\'.replace(",","."), unsafe_allow_html=True)
        with _k4:
            st.markdown(f\'\'\'<div style="background:#1e1e1e;border-radius:8px;padding:14px 16px;border-left:3px solid #F39C12;">
                <div style="font-size:10px;color:#8B9A2E;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">PROJ MES LIQUIDO</div>
                <div style="font-size:20px;font-weight:700;color:#F39C12;">R$ {_proj_liq:,.0f}</div>
                <div style="font-size:10px;color:#8B9A2E;margin-top:3px;">media R$ {_media_liq:,.0f}/dia</div>
            </div>\'\'\'.replace(",","."), unsafe_allow_html=True)

        st.markdown("<div style=\'height:16px\'></div>", unsafe_allow_html=True)

        # Grafico diario GMV vs Liquido
        import plotly.graph_objects as go
        _fig = go.Figure()
        _fig.add_trace(go.Bar(
            x=_df_kt["data"].astype(str), y=_df_kt["gmv"],
            name="GMV", marker_color="rgba(139,154,46,0.5)",
            hovertemplate="GMV: R$%{y:,.0f}<extra></extra>"
        ))
        _fig.add_trace(go.Bar(
            x=_df_kt["data"].astype(str), y=_df_kt["liquido"],
            name="Liquido", marker_color="#2ECC71",
            hovertemplate="Liquido: R$%{y:,.0f}<extra></extra>"
        ))
        _fig.update_layout(
            title="GMV vs Liquido por dia — Outubro 2026",
            barmode="overlay", height=320,
            plot_bgcolor="#1a1a1a", paper_bgcolor="#1a1a1a",
            font=dict(color="#C8BFB0", size=11),
            legend=dict(orientation="h", y=1.08),
            margin=dict(l=40,r=20,t=50,b=40),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)",
                       tickprefix="R$", tickformat=",.0f")
        )
        st.plotly_chart(_fig, use_container_width=True)

        # Tabela detalhada
        st.markdown(\'<div style="font-size:11px;color:#8B9A2E;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">DETALHE DIARIO</div>\', unsafe_allow_html=True)
        _df_show = _df_kt.copy()
        _df_show["margem"] = (_df_show["liquido"] / _df_show["gmv"] * 100).round(1).astype(str) + "%"
        _df_show["data"] = _df_show["data"].astype(str)
        _df_show = _df_show[["data","filial","gmv","liquido","margem","comissao","despesa","outras_despesas"]]
        _df_show.columns = ["Data","Filial","GMV","Liquido","Margem","Comissao","Despesa","Outras Desp"]
        _df_show["Filial"] = _df_show["Filial"].str.replace("Olive Garden - ","")
        for col in ["GMV","Liquido","Comissao","Despesa","Outras Desp"]:
            _df_show[col] = _df_show[col].apply(lambda x: f"R$ {float(x):,.0f}".replace(",","."))
        st.dataframe(_df_show, use_container_width=True, hide_index=True)

        # Nota resultado geral
        st.markdown(f\'\'\'<div style="background:rgba(139,154,46,0.08);border:1px solid rgba(139,154,46,0.25);border-radius:6px;padding:10px 14px;margin-top:12px;font-size:11px;color:#C8BFB0;">
            <b style="color:#8B9A2E;">Resultado Geral:</b> Keeta liquido MTD de <b>R$ {_tot_liq:,.0f}</b> ja incluido no faturamento total da rede na Visao Executiva.
        </div>\'\'\'.replace(",","."), unsafe_allow_html=True)

'''

# Inserir apos o bloco Fila
# Encontra o fim do arquivo e insere antes
t = t + KEETA_BLOCK
print("OK: bloco Keeta inserido")

p.write_text(t, encoding="utf-8")

import py_compile
py_compile.compile(str(p), doraise=True)
print("OK: compila sem erros")
