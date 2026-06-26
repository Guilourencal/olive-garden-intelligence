lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
# Corrigir linha 486 — remover virgula do final
lines[485] = '                f\'<div style="font-size:12px;color:#3D2B1F;line-height:1.5;">{str(row["comentario"])[:300]}{"..." if len(str(row["comentario"])) > 300 else ""}</div></div>\'\n'
# Remover linha 487 duplicada
del lines[486]
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
