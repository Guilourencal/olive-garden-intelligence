lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

novo = '''            # Layout 2x3 — grid CSS
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
            _pct_conc_ve = int(_dias_realizados_ve / _dias_no_mes_ve * 100) if _dias_no_mes_ve > 0 else 0
            fat_total_mtd = vt + fat_if_mtd
            fat_total_fmt2 = f"R$ {fat_total_mtd:,.0f}".replace(",",".")
            fat_if_fmt2 = f"R$ {fat_if_mtd:,.0f}".replace(",",".")
            pct_if2 = fat_if_mtd / fat_total_mtd * 100 if fat_total_mtd > 0 else 0
            ped_if2 = int(df_if_mtd["pedidos"].sum()) if len(df_if_mtd) > 0 else 0
            tm_if2 = fat_if_mtd / ped_if2 if ped_if2 > 0 else 0
            seta_m2 = "▲" if pct_meta >= 0 else "▼"
            cor_m2 = "#4CAF7D" if pct_meta >= 0 else "#E57373"
            seta_a2 = "▲" if pct_ano1 >= 0 else "▼"
            cor_a2 = "#4CAF7D" if pct_ano1 >= 0 else "#E57373"
            hdc_ve = df_vd_f["venda_por_hdc"].mean() if len(df_vd_f) > 0 else 0
            hdc_ve_fmt = f"R$ {hdc_ve:.0f}" if pd.notna(hdc_ve) else "—"
            if len(df_mes_ve) > 0:
                proj_if_ve = (fat_if_mtd / _dias_realizados_ve * (_dias_no_mes_ve - _dias_realizados_ve)) if _dias_realizados_ve > 0 else 0
                proj_total_ve = proj_total + proj_if_ve if "proj_total" in dir() else fat_total_mtd
                budget_ve = df_mes_ve["meta_venda"].sum() / _dias_realizados_ve * _dias_no_mes_ve if _dias_realizados_ve > 0 else 0
                pct_proj_ve = (proj_total_ve / budget_ve - 1) * 100 if budget_ve > 0 else 0
                cor_pv2 = "#4CAF7D" if pct_proj_ve >= 0 else "#E57373"
                seta_pv2 = "▲" if pct_proj_ve >= 0 else "▼"
                proj_ve_fmt = f"R$ {proj_total_ve:,.0f}".replace(",",".")
                budget_ve_fmt = f"R$ {budget_ve:,.0f}".replace(",",".")
                _proj_html = (
                    f\'<div style="font-size:30px;font-weight:800;margin-bottom:8px;letter-spacing:-0.5px;">{proj_ve_fmt}</div>\' +
                    f\'<div style="background:rgba(255,255,255,0.15);border-radius:3px;height:3px;margin-bottom:6px;">\' +
                    f\'<div style="background:#8B9A2E;width:{_pct_conc_ve}%;height:3px;border-radius:3px;"></div></div>\' +
                    f\'<div style="font-size:10px;color:#9DC88D;margin-bottom:8px;">{_dias_realizados_ve}/{_dias_no_mes_ve} dias realizados</div>\' +
                    f\'<div style="display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;">\' +
                    f\'<span style="font-size:10px;color:#9DC88D;">Budget: {budget_ve_fmt}</span>\' +
                    f\'<span style="font-size:14px;font-weight:800;color:{cor_pv2};">{seta_pv2} {pct_proj_ve:+.1f}%</span></div>\'
                )
            else:
                _proj_html = \'<div style="font-size:12px;color:#9DC88D;margin-top:16px;">Sem dados do mes atual.</div>\'

            st.markdown(f\'\'\'
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;width:100%;box-sizing:border-box;">
                <div style="background:#1a3320;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#9DC88D;letter-spacing:2px;margin-bottom:8px;">FATURAMENTO TOTAL MTD</div>
                    <div style="font-size:30px;font-weight:800;margin-bottom:8px;letter-spacing:-0.5px;">{fat_total_fmt2}</div>
                    <div style="font-size:10px;color:#9DC88D;margin-bottom:4px;">Salao: {vt_fmt} &nbsp;|&nbsp; iFood: {fat_if_fmt2}</div>
                    <div style="border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;font-size:10px;color:#9DC88D;">{pct_if2:.1f}% do faturamento via iFood</div>
                </div>
                <div style="background:#1a3320;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#9DC88D;letter-spacing:2px;margin-bottom:8px;">PROJECAO TOTAL DO MES</div>
                    {_proj_html}
                </div>
                <div style="background:#3D2B1F;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:8px;">OPERACAO SALAO</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px;">
                        <div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">GUEST COUNT</div><div style="font-size:24px;font-weight:800;">{gc_fmt}</div></div>
                        <div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">TICKET MEDIO</div><div style="font-size:24px;font-weight:800;color:#8B9A2E;">{tk_fmt}</div></div>
                        <div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">VENDA / HDC</div><div style="font-size:20px;font-weight:700;color:#8B9A2E;">{hdc_ve_fmt}</div></div>
                    </div>
                </div>
            </div>
            <div style="height:12px;"></div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;width:100%;box-sizing:border-box;">
                <div style="background:#3D2B1F;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:8px;">VENDA SALAO VS BUDGET</div>
                    <div style="font-size:28px;font-weight:800;margin-bottom:8px;">{vt_fmt}</div>
                    <div style="display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;">
                        <span style="font-size:10px;color:#D8CFC0;">Budget: {mt_fmt}</span>
                        <span style="font-size:16px;font-weight:800;color:{cor_m2};">{seta_m2} {pct_meta:+.1f}%</span>
                    </div>
                </div>
                <div style="background:#3D2B1F;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:8px;">VENDA SALAO VS ANO ANTERIOR</div>
                    <div style="font-size:28px;font-weight:800;margin-bottom:8px;">{vt_fmt}</div>
                    <div style="display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;">
                        <span style="font-size:10px;color:#D8CFC0;">AA: {va1_fmt}</span>
                        <span style="font-size:16px;font-weight:800;color:{cor_a2};">{seta_a2} {pct_ano1:+.1f}%</span>
                    </div>
                </div>
                <div style="background:#3D2B1F;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:8px;">IFOOD MTD</div>
                    <div style="font-size:28px;font-weight:800;margin-bottom:8px;">{fat_if_fmt2}</div>
                    <div style="display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;">
                        <span style="font-size:10px;color:#D8CFC0;">{ped_if2} pedidos</span>
                        <span style="font-size:12px;color:#8B9A2E;font-weight:700;">TM R$ {tm_if2:.0f}</span>
                    </div>
                </div>
            </div>
            \'\'\', unsafe_allow_html=True)

'''

lines[1041:1150] = [novo]
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print(f'OK — {len(lines)} linhas')
