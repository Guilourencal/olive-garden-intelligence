content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''        with col_e2:
            with st.container(border=True):
                st.markdown(
                    \'<div style="text-align:center; padding:8px;">\' +
                    \'<div style="font-size:9px; color:#8B7A5A; letter-spacing:2px; margin-bottom:4px;">REVENUE SCORE</div>\' +
                    f\'<div style="font-size:28px; font-weight:800; color:#3D2B1F;">R$ {rev_total/1000:.0f}k</div>\' +
                    f\'<div style="font-size:10px; color:#8B9A2E;">impacto real na receita</div></div>\',
                    unsafe_allow_html=True)'''

new = '''        with col_e2:
            with st.container(border=True):
                check_uplift_medio = df_mf[df_mf["check_uplift"].notna()]["check_uplift"].mean()
                cor_uplift = "#2e6b3e" if check_uplift_medio > 100 else "#B8923A"
                st.markdown(
                    \'<div style="text-align:center; padding:8px;">\' +
                    \'<div style="font-size:9px; color:#8B7A5A; letter-spacing:2px; margin-bottom:4px;">CHECK UPLIFT MEDIO</div>\' +
                    f\'<div style="font-size:28px; font-weight:800; color:{cor_uplift};">R$ {check_uplift_medio:.0f}</div>\' +
                    f\'<div style="font-size:10px; color:#8B7A5A;">valor extra gerado por check</div></div>\',
                    unsafe_allow_html=True)'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
