lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

lines[1998] = '        if len(resultados_proj) == 0:\n'
lines.insert(1999, '            st.warning("Sem dados suficientes para gerar projecoes.")\n')
lines.insert(2000, '        else:\n')

# Indentar as linhas seguintes que estavam no mesmo nivel
# Ver quantas linhas precisam ser indentadas
for i in range(2001, min(2060, len(lines))):
    if lines[i].startswith('        ') and not lines[i].startswith('            '):
        lines[i] = '    ' + lines[i]
    elif lines[i].startswith('    elif') or lines[i].startswith('    else') or lines[i] == '\n':
        break

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
