content = open('dashboard.py', 'r', encoding='utf-8').read()

# Fix 1 — Voz do Cliente (Buzzmonitor) com scroll
old = '        st.markdown(\'<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Reclamacoes reais — filtradas por unidade, tema e canal acima.</div>\', unsafe_allow_html=True)\n        df_voz = df_rf.sort_values("data", ascending=False).head(50)\n        for _, row in df_voz.iterrows():'
new = '        st.markdown(\'<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Reclamacoes reais do Buzzmonitor (Google + Instagram) — filtradas por unidade, tema e canal acima.</div>\', unsafe_allow_html=True)\n        df_voz = df_rf.sort_values("data", ascending=False).head(100)\n        html_voz = ""\n        for _, row in df_voz.iterrows():'

if old in content:
    content = content.replace(old, new)
    print('OK fix1a')
else:
    print('NAO ENCONTRADO fix1a')

open('dashboard.py', 'w', encoding='utf-8').write(content)
