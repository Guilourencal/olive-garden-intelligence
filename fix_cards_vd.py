lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')

novo_cards = [
    '            cols_c = st.columns(3)',
    '            # Card 1 - Venda Total vs Budget',
    '            with cols_c[0]:',
    '                seta_meta = "▲" if pct_meta >= 0 else "▼"',
    '                cor_meta2 = "#2e6b3e" if pct_meta >= 0 else "#c0392b"',
    '                st.markdown(f\'\'\'<div style="background:#3D2B1F; border-radius:10px; padding:20px; color:#F5F0E8;">',
    '                    <div style="font-size:9px; color:#D8CFC0; letter-spacing:2px; margin-bottom:12px;">VENDA TOTAL</div>',
    '                    <div style="font-size:28px; font-weight:800; margin-bottom:8px;">{vt_fmt}</div>',
    '                    <div style="display:flex; justify-content:space-between; align-items:center; padding-top:10px; border-top:1px solid rgba(255,255,255,0.1);">',
    '                    <div><div style="font-size:9px; color:#D8CFC0; margin-bottom:2px;">BUDGET</div>',
    '                    <div style="font-size:12px; color:#D8CFC0;">{mt_fmt}</div></div>',
    '                    <div style="font-size:18px; font-weight:700; color:{cor_meta2};">{seta_meta} {pct_meta:+.1f}%</div>',
    '                    </div></div>\'\'\', unsafe_allow_html=True)',
    '            # Card 2 - Venda vs Ano Anterior',
    '            with cols_c[1]:',
    '                seta_ano1 = "▲" if pct_ano1 >= 0 else "▼"',
    '                cor_ano12 = "#2e6b3e" if pct_ano1 >= 0 else "#c0392b"',
    '                st.markdown(f\'\'\'<div style="background:#3D2B1F; border-radius:10px; padding:20px; color:#F5F0E8;">',
    '                    <div style="font-size:9px; color:#D8CFC0; letter-spacing:2px; margin-bottom:12px;">VENDA TOTAL</div>',
    '                    <div style="font-size:28px; font-weight:800; margin-bottom:8px;">{vt_fmt}</div>',
    '                    <div style="display:flex; justify-content:space-between; align-items:center; padding-top:10px; border-top:1px solid rgba(255,255,255,0.1);">',
    '                    <div><div style="font-size:9px; color:#D8CFC0; margin-bottom:2px;">ANO ANTERIOR</div>',
    '                    <div style="font-size:12px; color:#D8CFC0;">{va1_fmt}</div></div>',
    '                    <div style="font-size:18px; font-weight:700; color:{cor_ano12};">{seta_ano1} {pct_ano1:+.1f}%</div>',
    '                    </div></div>\'\'\', unsafe_allow_html=True)',
    '            # Card 3 - Guest Count e Ticket',
    '            with cols_c[2]:',
    '                st.markdown(f\'\'\'<div style="background:#3D2B1F; border-radius:10px; padding:20px; color:#F5F0E8;">',
    '                    <div style="font-size:9px; color:#D8CFC0; letter-spacing:2px; margin-bottom:12px;">OPERACAO</div>',
    '                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:8px;">',
    '                    <div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">GUEST COUNT</div>',
    '                    <div style="font-size:22px; font-weight:800;">{int(gc):,}".replace(",",".")</div></div>',
    '                    <div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">TICKET MEDIO</div>',
    '                    <div style="font-size:22px; font-weight:800; color:#8B9A2E;">{tk_fmt}</div></div>',
    '                    </div></div>\'\'\', unsafe_allow_html=True)',
]

# Substituir linhas 1093 a 1108
result = lines[:1093] + novo_cards + lines[1108:]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result))
print(f'Feito! Total: {len(result)} linhas')
