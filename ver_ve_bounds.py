lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if '# Layout 2x3 — grid CSS' in line or 'col_ve4, col_ve5, col_ve6' in line or "st.markdown(\"<br>\", unsafe_allow_html=True)\n" == line and i > 1040:
        print(f'{i+1}: {line}', end='')
