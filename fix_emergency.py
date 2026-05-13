lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i in range(len(lines)):
    if 'padding:10px 0; border-bottom:1px solid #e8ddc8;' in lines[i]:
        lines[i] = '                st.markdown(f\'<div style="padding:10px 0; border-bottom:1px solid #e8ddc8;"><div style="display:flex; justify-content:space-between; align-items:center;"><span style="font-size:13px; font-weight:700; color:#3D2B1F;">{row["filial_curta"]}</span><span style="font-size:12px; color:{cor}; font-weight:700;">{div:+.1f} pts</span></div><div style="font-size:11px; color:#8B7A5A; margin-top:3px;">GSS: {row["overall_experience"]:.1f}% | Rep: {row["score_externo"]:.1f} | {msg}</div></div>\', unsafe_allow_html=True)'
        del lines[i+1:i+7]
        print(f'Linha {i+1} corrigida!')
        break
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
