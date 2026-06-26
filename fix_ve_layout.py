lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

novo_bloco = '''            # Layout 2x3
            import calendar as _cal_ve
            from datetime import date as _date_ve2
            _hoje_ve2 = _date_ve2.today()
            _dias_no_mes_ve = _cal_ve.monthrange(_hoje_ve2.year, _hoje_ve2.month)[1]
            df_mes_ve = df_vd[
                (df_vd["data"].dt.month == _hoje_ve2.month) &
                (df_vd["data"].dt.year == _hoje_ve2.year) &
                df_vd["filial_curta"].isin(filiais_sel)
            ].copy()
            _dias_realizados_ve = int(df_mes_ve["data"].dt.day.max()) if len(df_mes_ve) > 0 else 0
            _pct_concluido_ve = int(_dias_realizados_ve / _dias_no_mes_ve * 100) if _dias_no_mes_ve > 0 else 0

            # Linha 1 — totais e projecao
            col_ve1, col_ve2, col_ve3 = st.columns(3)
            with col_ve1:
                fat_total_mtd = vt + fat_if_mtd
                fat_total_fmt2 = f"R$ {fat_total_mtd:,.0f}".replace(",",".")
                fat_if_fmt2 = f"R$ {fat_if_mtd:,.0f}".replace(",",".")
                pct_if = fat_if_mtd / fat_total_mtd * 100 if fat_total_mtd > 0 else 0
                st.markdown(
                    f\'<div style="background:#1a3320;border-radius:12px;padding:20px;color:#F5F0E8;min-height:130px;">\' +
                    \'<div style="font-size:9px;color:#9DC88D;letter-spacing:2px;margin-bottom:8px;">FATURAMENTO TOTAL MTD</div>\' +
                    f\'<div style="font-size:32px;font-weight:800;margin-bottom:6px;">{fat_total_fmt2}</div>\' +
                    f\'<div style="display:flex;gap:16px;font-size:10px;color:#9DC88D;">\' +
                    f\'<span>Salao: {vt_fmt}</span><span>iFood: {fat_if_fmt2}</span></div>\' +
                    f\'<div style="font-size:10px;color:#9DC88D;margin-top:4px;">{pct_if:.1f}% via iFood</div></div>\',
                    unsafe_allow_html=True)
            with col_ve2:
                if len(df_mes_ve) > 0:
                    proj_if_ve = (fat_if_mtd / _dias_realizados_ve * (_dias_no_mes_ve - _dias_realizados_ve)) if _dias_realizados_ve > 0 else 0
                    proj_total_ve = proj_total + proj_if_ve if "proj_total" in dir() else fat_total_mtd
                    budget_ve = df_mes_ve["meta_venda"].sum() / _dias_realizados_ve * _dias_no_mes_ve if _dias_realizados_ve > 0 else 0
                    pct_proj_ve = (proj_total_ve / budget_ve - 1) * 100 if budget_ve > 0 else 0
                    cor_pv = "#8B9A2E" if pct_proj_ve >= 0 else "#c0392b"
                    seta_pv = "▲" if pct_proj_ve >= 0 else "▼"
                    proj_ve_fmt = f"R$ {proj_total_ve:,.0f}".replace(",",".")
                    budget_ve_fmt = f"R$ {budget_ve:,.0f}".replace(",",".")
                    st.markdown(
                        f\'<div style="background:#1a3320;border-radius:12px;padding:20px;color:#F5F0E8;min-height:130px;">\' +
                        \'<div style="font-size:9px;color:#9DC88D;letter-spacing:2px;margin-bottom:8px;">PROJECAO TOTAL DO MES</div>\' +
                        f\'<div style="font-size:32px;font-weight:800;margin-bottom:6px;">{proj_ve_fmt}</div>\' +
                        f\'<div style="background:rgba(255,255,255,0.15);border-radius:4px;height:4px;margin-bottom:6px;">\' +
                        f\'<div style="background:#8B9A2E;width:{_pct_concluido_ve}%;height:4px;border-radius:4px;"></div></div>\' +
                        f\'<div style="display:flex;justify-content:space-between;font-size:10px;color:#9DC88D;">\' +
                        f\'<span>{_dias_realizados_ve}/{_dias_no_mes_ve} dias realizados</span>\' +
                        f\'<span style="color:{cor_pv};font-weight:700;">{seta_pv} {pct_proj_ve:+.1f}% vs budget</span></div></div>\',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        \'<div style="background:#1a3320;border-radius:12px;padding:20px;color:#F5F0E8;min-height:130px;">\' +
                        \'<div style="font-size:9px;color:#9DC88D;letter-spacing:2px;margin-bottom:8px;">PROJECAO TOTAL DO MES</div>\' +
                        \'<div style="font-size:13px;color:#9DC88D;margin-top:16px;">Sem dados do mes atual.</div></div>\',
                        unsafe_allow_html=True)
            with col_ve3:
                hdc_medio_ve = df_vd_f["venda_por_hdc"].mean() if len(df_vd_f) > 0 else 0
                hdc_fmt_ve = f"R$ {hdc_medio_ve:.0f}" if pd.notna(hdc_medio_ve) else "—"
                st.markdown(
                    f\'<div style="background:#3D2B1F;border-radius:12px;padding:20px;color:#F5F0E8;min-height:130px;">\' +
                    \'<div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:8px;">OPERACAO SALAO</div>\' +
                    f\'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:4px;">\' +
                    \'<div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">GUEST COUNT</div>\' +
                    f\'<div style="font-size:24px;font-weight:800;">{gc_fmt}</div></div>\' +
                    \'<div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">TICKET MEDIO</div>\' +
                    f\'<div style="font-size:24px;font-weight:800;color:#8B9A2E;">{tk_fmt}</div></div>\' +
                    \'<div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">VENDA/HDC</div>\' +
                    f\'<div style="font-size:20px;font-weight:700;color:#8B9A2E;">{hdc_fmt_ve}</div></div>\' +
                    \'</div></div>\',
                    unsafe_allow_html=True)

            st.markdown("<div style=\'height:12px\'></div>", unsafe_allow_html=True)

            # Linha 2 — comparativos
            col_ve4, col_ve5, col_ve6 = st.columns(3)
            with col_ve4:
                seta_m = "▲" if pct_meta >= 0 else "▼"
                cor_m = "#2e6b3e" if pct_meta >= 0 else "#c0392b"
                st.markdown(
                    f\'<div style="background:#3D2B1F;border-radius:12px;padding:16px;color:#F5F0E8;">\' +
                    \'<div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:6px;">VENDA SALAO VS BUDGET</div>\' +
                    f\'<div style="font-size:26px;font-weight:800;margin-bottom:6px;">{vt_fmt}</div>\' +
                    f\'<div style="display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,0.1);padding-top:8px;">\' +
                    f\'<span style="font-size:11px;color:#D8CFC0;">Budget: {mt_fmt}</span>\' +
                    f\'<span style="font-size:16px;font-weight:700;color:{cor_m};">{seta_m} {pct_meta:+.1f}%</span></div></div>\',
                    unsafe_allow_html=True)
            with col_ve5:
                seta_a = "▲" if pct_ano1 >= 0 else "▼"
                cor_a = "#2e6b3e" if pct_ano1 >= 0 else "#c0392b"
                st.markdown(
                    f\'<div style="background:#3D2B1F;border-radius:12px;padding:16px;color:#F5F0E8;">\' +
                    \'<div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:6px;">VENDA SALAO VS ANO ANTERIOR</div>\' +
                    f\'<div style="font-size:26px;font-weight:800;margin-bottom:6px;">{vt_fmt}</div>\' +
                    f\'<div style="display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,0.1);padding-top:8px;">\' +
                    f\'<span style="font-size:11px;color:#D8CFC0;">AA: {va1_fmt}</span>\' +
                    f\'<span style="font-size:16px;font-weight:700;color:{cor_a};">{seta_a} {pct_ano1:+.1f}%</span></div></div>\',
                    unsafe_allow_html=True)
            with col_ve6:
                ped_if = int(df_if_mtd["pedidos"].sum()) if len(df_if_mtd) > 0 else 0
                tm_if = fat_if_mtd / ped_if if ped_if > 0 else 0
                fat_if_fmt3 = f"R$ {fat_if_mtd:,.0f}".replace(",",".")
                st.markdown(
                    f\'<div style="background:#3D2B1F;border-radius:12px;padding:16px;color:#F5F0E8;">\' +
                    \'<div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:6px;">IFOOD MTD</div>\' +
                    f\'<div style="font-size:26px;font-weight:800;margin-bottom:6px;">{fat_if_fmt3}</div>\' +
                    f\'<div style="display:flex;gap:16px;border-top:1px solid rgba(255,255,255,0.1);padding-top:8px;">\' +
                    f\'<span style="font-size:11px;color:#D8CFC0;">{ped_if} pedidos</span>\' +
                    f\'<span style="font-size:11px;color:#8B9A2E;">TM R$ {tm_if:.0f}</span></div></div>\',
                    unsafe_allow_html=True)
'''

lines[1041:1192] = [novo_bloco]
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print(f'OK — {len(lines)} linhas')
