content = open('dashboard.py', 'r', encoding='utf-8').read()

old = "                else:\n                    st.markdown('''<div style=\"background:#3D2B1F; border-radius:10px; padding:20px; color:#F5F0E8;\">\n                        <div style=\"font-size:9px; color:#D8CFC0; letter-spacing:2px; margin-bottom:12px;\">PROJECAO DO MES</div>\n                        <div style=\"font-size:13px; color:#8B7A5A;\">Selecione o mes atual para ver a projecao.</div>\n                        </div>''', unsafe_allow_html=True)"
new = """                else:
                    st.markdown(\'\'\'<div style="background:#3D2B1F; border-radius:10px; padding:20px; color:#F5F0E8;">
                        <div style="font-size:9px; color:#D8CFC0; letter-spacing:2px; margin-bottom:12px;">PROJECAO DO MES</div>
                        <div style="font-size:13px; color:#8B7A5A;">Selecione o mes atual para ver a projecao.</div>
                        </div>\'\'\', unsafe_allow_html=True)
            # Card 5 — Faturamento Total MTD
            with cols_c[4]:
                fat_total_mtd = vt + fat_if_mtd if "vt" in dir() else fat_if_mtd
                fat_total_fmt = f"R$ {fat_total_mtd:,.0f}".replace(",",".")
                fat_if_fmt = f"R$ {fat_if_mtd:,.0f}".replace(",",".")
                st.markdown(f\'\'\'<div style="background:#1a3320; border-radius:10px; padding:20px; color:#F5F0E8;">
                    <div style="font-size:9px; color:#9DC88D; letter-spacing:2px; margin-bottom:12px;">FATURAMENTO TOTAL MTD</div>
                    <div style="font-size:28px; font-weight:800; margin-bottom:8px;">{fat_total_fmt}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center; padding-top:10px; border-top:1px solid rgba(255,255,255,0.1);">
                    <div><div style="font-size:9px; color:#9DC88D; margin-bottom:2px;">IFOOD MTD</div>
                    <div style="font-size:12px; color:#9DC88D;">{fat_if_fmt}</div></div>
                    <div style="font-size:11px; color:#9DC88D;">Salao + iFood</div>
                    </div></div>\'\'\', unsafe_allow_html=True)
            # Card 6 — Projecao Total
            with cols_c[5]:
                if len(df_mes_atual) > 0:
                    import calendar as _cal
                    _dias_no_mes = _cal.monthrange(_hoje_ve.year, _hoje_ve.month)[1]
                    _dias_realizados = df_mes_atual["data"].dt.day.max()
                    _dias_restantes = _dias_no_mes - _dias_realizados
                    proj_if_restante = (fat_if_mtd / _dias_realizados * _dias_restantes) if _dias_realizados > 0 else 0
                    proj_total_geral = proj_total + proj_if_restante if "proj_total" in dir() else fat_total_mtd
                    proj_total_geral_fmt = f"R$ {proj_total_geral:,.0f}".replace(",",".")
                    budget_total_fmt = f"R$ {budget_mes:,.0f}".replace(",",".") if "budget_mes" in dir() else "—"
                    pct_proj_total = (proj_total_geral / budget_mes - 1) * 100 if "budget_mes" in dir() and budget_mes > 0 else 0
                    seta_pt = "▲" if pct_proj_total >= 0 else "▼"
                    cor_pt = "#2e6b3e" if pct_proj_total >= 0 else "#c0392b"
                    st.markdown(f\'\'\'<div style="background:#1a3320; border-radius:10px; padding:20px; color:#F5F0E8;">
                        <div style="font-size:9px; color:#9DC88D; letter-spacing:2px; margin-bottom:12px;">PROJECAO TOTAL MES</div>
                        <div style="font-size:24px; font-weight:800; margin-bottom:8px;">{proj_total_geral_fmt}</div>
                        <div style="background:rgba(255,255,255,0.1); border-radius:4px; height:4px; margin-bottom:8px;">
                            <div style="background:#8B9A2E; width:{pct_concluido}%; height:4px; border-radius:4px;"></div>
                        </div>
                        <div style="font-size:9px; color:#9DC88D; margin-bottom:8px;">{_dias_realizados}/{_dias_no_mes} dias | iFood projetado</div>
                        <div style="display:flex; justify-content:space-between; align-items:center; padding-top:10px; border-top:1px solid rgba(255,255,255,0.1);">
                        <div><div style="font-size:9px; color:#9DC88D; margin-bottom:2px;">BUDGET MES</div>
                        <div style="font-size:12px; color:#9DC88D;">{budget_total_fmt}</div></div>
                        <div style="font-size:18px; font-weight:700; color:{cor_pt};">{seta_pt} {pct_proj_total:+.1f}%</div>
                        </div></div>\'\'\', unsafe_allow_html=True)
                else:
                    st.markdown(\'\'\'<div style="background:#1a3320; border-radius:10px; padding:20px; color:#F5F0E8;">
                        <div style="font-size:9px; color:#9DC88D; letter-spacing:2px; margin-bottom:12px;">PROJECAO TOTAL MES</div>
                        <div style="font-size:13px; color:#8B7A5A;">Selecione o mes atual para ver a projecao.</div>
                        </div>\'\'\', unsafe_allow_html=True)"""

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK step 2')
else:
    print('TRECHO NAO ENCONTRADO step 2')
