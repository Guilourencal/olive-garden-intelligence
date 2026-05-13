lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
old = '                st.markdown(f\'<div style="padding:10px 0; border-bottom:1px solid #e8ddc8;">\n                    <div style="display:flex; justify-content:space-between; align-items:center;">\n                    <span style="font-size:13px; font-weight:700; color:#3D2B1F;">{row["filial_curta"]}</span>\n                    <span style="font-size:12px; color:{cor}; font-weight:700;">{div:+.1f} pts \xe2\x80\x94 {icone}</span>\n                    </div>\n                    <div style="font-size:11px; color:#8B7A5A; margin-top:3px;">GSS: {row["overall_experience"]:.1f}% | Reputacao: {row["score_externo"]:.1f} | {msg}</div>\n                    </div>\', unsafe_allow_html=True)'
new = '                st.markdown(f\'<div style="padding:10px 0; border-bottom:1px solid #e8ddc8;"><div style="display:flex; justify-content:space-between; align-items:center;"><span style="font-size:13px; font-weight:700; color:#3D2B1F;">{row["filial_curta"]}</span><span style="font-size:12px; color:{cor}; font-weight:700;">{div:+.1f} pts</span></div><div style="font-size:11px; color:#8B7A5A; margin-top:3px;">GSS: {row["overall_experience"]:.1f}% | Reputacao: {row["score_externo"]:.1f} | {msg}</div></div>\', unsafe_allow_html=True)'
content = '\n'.join(lines)
if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('Feito!')
else:
    lines[1185] = '                st.markdown(f\'<div style="padding:10px 0; border-bottom:1px solid #e8ddc8;"><div style="display:flex; justify-content:space-between;"><span style="font-size:13px; font-weight:700; color:#3D2B1F;">{row["filial_curta"]}</span><span style="font-size:12px; color:{cor}; font-weight:700;">{div:+.1f} pts — {icone}</span></div><div style="font-size:11px; color:#8B7A5A; margin-top:3px;">GSS: {row["overall_experience"]:.1f}% | Rep: {row["score_externo"]:.1f} | {msg}</div></div>\', unsafe_allow_html=True)'
    del lines[1186:1192]
    open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
    print('Corrigido por linha!')
