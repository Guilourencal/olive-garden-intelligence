lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'cols_proj = st.columns(len(resultados_proj))' in line:
        lines[i] = '        cols_proj = st.columns(max(len(resultados_proj), 1))\n'
        print(f'Corrigido linha {i+1}')
        break
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
