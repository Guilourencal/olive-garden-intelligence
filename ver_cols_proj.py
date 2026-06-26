lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'cols_proj = st.columns(len(resultados_proj))' in line:
        print(f'{i+1}: {line}', end='')
