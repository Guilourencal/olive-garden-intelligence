content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''                st.markdown(
                f\'<div style="padding:12px 0;border-bottom:1px solid #e8ddc8;">\' +
                f\'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">\' +
                f\'<div style="display:flex;gap:8px;align-items:center;">\' +
                f\'<span style="font-size:10px;font-weight:700;color:#3D2B1F;">{row["unidade_curta"]}</span>\' +
                f\'<span style="font-size:9px;background:#e8ddc8;color:#3D2B1F;padding:2px 6px;border-radius:4px;">{tema_badge}</span>\' +
                (f\'<span style="font-size:9px;background:#f5e8e8;color:#8B2E2E;padding:2px 6px;border-radius:4px;">{subtema_badge}</span>\' if subtema_badge else "") +
                f\'</div>\' +
                f\'<div style="display:flex;gap:8px;align-items:center;">\' +
                f\'<span style="font-size:11px;color:{cor_nota_v};font-weight:700;">{estrelas}</span>\' +
                f\'<span style="font-size:10px;color:#8B7A5A;">{canal_icon} {str(row["data"])[:10]}</span>\' +
                f\'</div></div>\' +
                f\'<div style="font-size:12px;color:#3D2B1F;line-height:1.5;">{str(row["comentario"])[:300]}{"..." if len(str(row["comentario"])) > 300 else ""}</div></div>\',
                unsafe_allow_html=True)'''

new = '''                html_voz += (
                f\'<div style="padding:12px 0;border-bottom:1px solid #e8ddc8;">\' +
                f\'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">\' +
                f\'<div style="display:flex;gap:8px;align-items:center;">\' +
                f\'<span style="font-size:10px;font-weight:700;color:#3D2B1F;">{row["unidade_curta"]}</span>\' +
                f\'<span style="font-size:9px;background:#e8ddc8;color:#3D2B1F;padding:2px 6px;border-radius:4px;">{tema_badge}</span>\' +
                (f\'<span style="font-size:9px;background:#f5e8e8;color:#8B2E2E;padding:2px 6px;border-radius:4px;">{subtema_badge}</span>\' if subtema_badge else "") +
                f\'</div>\' +
                f\'<div style="display:flex;gap:8px;align-items:center;">\' +
                f\'<span style="font-size:11px;color:{cor_nota_v};font-weight:700;">{estrelas}</span>\' +
                f\'<span style="font-size:10px;color:#8B7A5A;">{canal_icon} {str(row["data"])[:10]}</span>\' +
                f\'</div></div>\' +
                f\'<div style="font-size:12px;color:#3D2B1F;line-height:1.5;">{str(row["comentario"])[:300]}{"..." if len(str(row["comentario"])) > 300 else ""}</div></div>\'
                )
        st.markdown(f\'<div style="height:420px;overflow-y:auto;padding-right:8px;">{html_voz}</div>\', unsafe_allow_html=True)'''

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK fix1b')
else:
    print('NAO ENCONTRADO fix1b')
