content = open('dashboard.py', 'r', encoding='utf-8').read()

old = "            st.markdown('<div class=\"section-title\">Visao Executiva — Salao + iFood</div>', unsafe_allow_html=True)"
new = "            st.markdown('<div class=\"section-title\">Visao Executiva</div>', unsafe_allow_html=True)"

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK titulo')
else:
    print('TRECHO NAO ENCONTRADO')
