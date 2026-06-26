lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

# Substituir st.markdown por html_voz += e adicionar scroll no final
lines[473] = '            html_voz += (\n'
lines[474] = '                f\'<div style="padding:12px 0;border-bottom:1px solid #e8ddc8;">\' +\n'
lines[486] = '                f\'<div style="font-size:12px;color:#3D2B1F;line-height:1.5;">{str(row["comentario"])[:300]}{"..." if len(str(row["comentario"])) > 300 else ""}</div></div>\'\n'
lines[487] = '            )\n'
lines[488] = '        st.markdown(f\'<div style="height:420px;overflow-y:auto;padding-right:8px;">{html_voz}</div>\', unsafe_allow_html=True)\n'

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
