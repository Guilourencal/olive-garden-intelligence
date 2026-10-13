import pathlib, py_compile, re

p = pathlib.Path("dashboard.py")
t = p.read_text(encoding="utf-8")

# 1. Remover "Keeta" da sidebar (desfaz add_aba_keeta.py)
OLD_ABAS = '["Reviews", "Social", "Pesquisa", "Analises", "Vendas", "OlivIA", "Menu", "Fila", "Keeta"]'
NEW_ABAS = '["Reviews", "Social", "Pesquisa", "Analises", "Vendas", "OlivIA", "Menu", "Fila"]'
if OLD_ABAS in t:
    t = t.replace(OLD_ABAS, NEW_ABAS, 1)
    print("OK: Keeta removido da sidebar")
else:
    print("AVISO: sidebar ja estava sem Keeta")

# 2. Remover bloco aba Keeta que foi appendado no fim do arquivo
KEETA_ANCHOR = '\n# ============================================================\n# ABA KEETA\n# ============================================================\nif aba_sel == "Keeta":'
if KEETA_ANCHOR in t:
    idx = t.index(KEETA_ANCHOR)
    t = t[:idx]
    print("OK: bloco aba Keeta removido do fim do arquivo")
else:
    print("AVISO: bloco aba Keeta nao encontrado")

# 3. Adicionar "Keeta" no radio de Vendas
OLD_RADIO = '["Operacao Geral", "iFood"]'
NEW_RADIO = '["Operacao Geral", "iFood", "Keeta"]'
if OLD_RADIO in t:
    t = t.replace(OLD_RADIO, NEW_RADIO, 1)
    print("OK: Keeta adicionado no radio Vendas")
else:
    print("ERRO: radio Vendas nao encontrado")

# 4. Inserir bloco Keeta apos o bloco iFood (antes do proximo elif/else no mesmo nivel)
IFOOD_ANCHOR = '    elif visao_sel == "iFood":'
assert IFOOD_ANCHOR in t, "Ancora iFood nao encontrada"

# Encontrar fim do bloco iFood: proxima linha com mesma indentacao (4 espacos) apos o bloco
idx_ifood = t.rindex(IFOOD_ANCHOR)  # ultima ocorrencia
# Encontrar fim: procurar por linha com exatamente 4 espacos de indent que seja elif/else/if no mesmo nivel
# Ou fim do arquivo
after = t[idx_ifood:]
# Bloco Keeta a inserir no final do arquivo (depois do bloco iFood)
KEETA_BLOCK = '''
    elif visao_sel == "Keeta":
        import calendar as _kcal
        from datetime import datetime as _kdt, date as _kdate
        _khoje = _kdate.today()
        _kmes, _kano = _khoje.month, _khoje.year
        _kdias_mes = _kcal.monthrange(_kano, _kmes)[1]

        with get_conn() as _kconn:
            _df_kt = pd.read_sql(f"""
                SELECT data, filial,
                       vendas_itens as gmv,
                       ganhos_liquidos as liquido,
                       comissao, despesa, outras_despesas
                FROM keeta_diario
                WHERE EXTRACT(month FROM data)={_kmes}
                  AND EXTRACT(year FROM data)={_kano}
                ORDER BY data
            """, _kconn)
            _df_kt_hist = pd.read_sql("""
                SELECT DATE_TRUNC(\'month\', data)::date as mes,
                       SUM(ganhos_liquidos) as liquido,
                       SUM(vendas_itens) as gmv
                FROM keeta_diario
                GROUP BY 1 ORDER BY 1
            """, _kconn)

        with st.container(border=True):
            st.markdown(\'<div class="section-title">Visao Executiva — Keeta</div>\', unsafe_allow_html=True)

            if _df_kt.empty:
                st.info("Nenhum dado Keeta importado para este mes.")
            else:
                _ktot_gmv  = float(_df_kt["gmv"].sum())
                _ktot_liq  = float(_df_kt["liquido"].sum())
                _ktot_com  = float(_df_kt["comissao"].sum())
                _ktot_desp = float((_df_kt["despesa"] + _df_kt["outras_despesas"]).sum())
                _kdias_real = int(_df_kt["data"].nunique())
                _kmedia_liq = _ktot_liq / _kdias_real if _kdias_real > 0 else 0
                _kproj_liq  = _ktot_liq + _kmedia_liq * (_kdias_mes - _kdias_real)
                _kmargem    = _ktot_liq / _ktot_gmv * 100 if _ktot_gmv > 0 else 0
                _kproj_gmv  = _ktot_gmv + (_ktot_gmv / _kdias_real * (_kdias_mes - _kdias_real)) if _kdias_real > 0 else 0

                _kcols = st.columns(2)
                with _kcols[0]:
                    _kproj_html = ""
                    if _kdias_real < _kdias_mes:
                        _kproj_html = (
                            \'<div style="margin-top:12px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.1);">\'
                            + \'<div style="font-size:9px;color:#B8923A;letter-spacing:2px;margin-bottom:6px;">PROJECAO MES COMPLETO (\' + str(_kdias_mes) + \' dias)</div>\'
                            + \'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">\'
                            + \'<div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">GMV</div>\'
                            + \'<div style="font-size:14px;font-weight:700;color:#B8923A;">R$ \' + f"{_kproj_gmv:,.0f}".replace(",",".") + \'</div></div>\'
                            + \'<div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">LIQUIDO</div>\'
                            + \'<div style="font-size:14px;font-weight:700;color:#B8923A;">R$ \' + f"{_kproj_liq:,.0f}".replace(",",".") + \'</div></div>\'
                            + \'</div>\'
                            + \'<div style="font-size:9px;color:#8B7A5A;margin-top:4px;">Parcial: \' + str(_kdias_real) + \' de \' + str(_kdias_mes) + \' dias</div></div>\'
                        )
                    st.markdown(
                        \'<div style="background:#1a1209;border-radius:12px;padding:20px;color:#F5F0E8;margin-bottom:8px;border:1px solid #8B9A2E;">\'
                        + \'<div style="font-size:10px;letter-spacing:3px;color:#8B9A2E;text-transform:uppercase;margin-bottom:14px;">MTD — \' + _kdt.now().strftime("%b/%Y").upper() + \'</div>\'
                        + \'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">\'
                        + \'<div><div style="font-size:9px;color:#D8CFC0;margin-bottom:4px;">GMV</div>\'
                        + \'<div style="font-size:22px;font-weight:800;">R$ \' + f"{_ktot_gmv:,.0f}".replace(",",".") + \'</div></div>\'
                        + \'<div><div style="font-size:9px;color:#D8CFC0;margin-bottom:4px;">LIQUIDO</div>\'
                        + \'<div style="font-size:22px;font-weight:800;color:#8B9A2E;">R$ \' + f"{_ktot_liq:,.0f}".replace(",",".") + \'</div></div>\'
                        + \'<div><div style="font-size:9px;color:#D8CFC0;margin-bottom:4px;">MARGEM</div>\'
                        + \'<div style="font-size:18px;font-weight:700;color:#8B9A2E;">\' + f"{_kmargem:.1f}%" + \'</div></div>\'
                        + \'<div><div style="font-size:9px;color:#D8CFC0;margin-bottom:4px;">COMISSAO + DESP</div>\'
                        + \'<div style="font-size:18px;font-weight:700;color:#E74C3C;">R$ \' + f"{abs(_ktot_com+_ktot_desp):,.0f}".replace(",",".") + \'</div></div>\'
                        + \'</div>\' + _kproj_html + \'</div>\',
                        unsafe_allow_html=True)

                with _kcols[1]:
                    import plotly.graph_objects as _kgo
                    _kfig = _kgo.Figure()
                    _kfig.add_trace(_kgo.Bar(
                        x=_df_kt["data"].astype(str), y=_df_kt["gmv"],
                        name="GMV", marker_color="rgba(139,154,46,0.4)",
                        hovertemplate="GMV: R$%{y:,.0f}<extra></extra>"
                    ))
                    _kfig.add_trace(_kgo.Bar(
                        x=_df_kt["data"].astype(str), y=_df_kt["liquido"],
                        name="Liquido", marker_color="#8B9A2E",
                        hovertemplate="Liquido: R$%{y:,.0f}<extra></extra>"
                    ))
                    _kfig.update_layout(
                        barmode="overlay", height=220,
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#C8BFB0", size=10),
                        legend=dict(orientation="h", y=1.1, font=dict(size=9)),
                        margin=dict(l=30,r=10,t=10,b=30),
                        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=8)),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.04)",
                                   tickprefix="R$", tickformat=",.0f", tickfont=dict(size=9))
                    )
                    st.plotly_chart(_kfig, use_container_width=True)

        # Tabela detalhada
        with st.container(border=True):
            st.markdown(\'<div class="section-title">Detalhe Diario</div>\', unsafe_allow_html=True)
            if not _df_kt.empty:
                _df_show = _df_kt.copy()
                _df_show["Margem"] = (_df_show["liquido"] / _df_show["gmv"] * 100).round(1).astype(str) + "%"
                _df_show["Deducoes"] = _df_show["comissao"] + _df_show["despesa"] + _df_show["outras_despesas"]
                _df_show["data"] = _df_show["data"].astype(str)
                _df_show["filial"] = _df_show["filial"].str.replace("Olive Garden - ","")
                for col in ["gmv","liquido","Deducoes"]:
                    _df_show[col] = _df_show[col].apply(lambda x: f"R$ {float(x):,.0f}".replace(",","."))
                _df_show = _df_show.rename(columns={"data":"Data","filial":"Filial","gmv":"GMV","liquido":"Liquido"})
                st.dataframe(_df_show[["Data","Filial","GMV","Liquido","Margem","Deducoes"]], use_container_width=True, hide_index=True)

'''

# Inserir antes do proximo bloco de nivel igual apos iFood, ou no fim da secao Vendas
# Estrategia: inserir no fim do arquivo (antes do bloco Fila se existir no mesmo nivel)
# Encontrar "elif aba_sel ==" depois do bloco iFood
idx_depois = t.find('\nelif aba_sel ==', idx_ifood + 10)
if idx_depois > 0:
    t = t[:idx_depois] + KEETA_BLOCK + t[idx_depois:]
    print("OK: bloco Keeta inserido dentro de Vendas (antes do proximo elif aba_sel)")
else:
    t = t + KEETA_BLOCK
    print("OK: bloco Keeta inserido no fim do arquivo")

p.write_text(t, encoding="utf-8")
py_compile.compile(str(p), doraise=True)
print("OK: compila sem erros")
