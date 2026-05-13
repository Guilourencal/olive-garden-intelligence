lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
i = 0
while i < len(lines):
    if 'padding:10px 0; border-bottom:1px solid #e8ddc8;' in lines[i] and lines[i].strip().startswith('st.markdown'):
        lines[i] = '                st.markdown(f\'<div style="padding:10px 0; border-bottom:1px solid #e8ddc8;"><div style="display:flex; justify-content:space-between; align-items:center;"><span style="font-size:13px; font-weight:700; color:#3D2B1F;">{row["filial_curta"]}</span><span style="font-size:12px; color:{cor}; font-weight:700;">{div:+.1f} pts</span></div><div style="font-size:11px; color:#8B7A5A; margin-top:3px;">GSS: {row["overall_experience"]:.1f}% | Rep: {row["score_externo"]:.1f} | {msg}</div></div>\', unsafe_allow_html=True)'
        j = i + 1
        while j < len(lines) and lines[j].strip() in ['</div>\'\'\'', 'unsafe_allow_html=True', ')', 'f\'</div>\'', '']:
            if lines[j].strip() in ['unsafe_allow_html=True', ')'] or '</div>' in lines[j]:
                del lines[j]
            else:
                j += 1
        print(f'Corrigido linha {i+1}')
    i += 1
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(lines))
