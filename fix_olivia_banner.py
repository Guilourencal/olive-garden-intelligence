import base64

with open('static/olivia_banner.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if 'elif aba_sel == "OlivIA":' in l)
idx_fim = next(i for i in range(idx, idx+25) if '# Inicializar historico' in lines[i])

novo_header = [
    'elif aba_sel == "OlivIA":\n',
    '    import anthropic as _anthropic\n',
    '    import json as _json\n',
    '    with open("static/olivia_banner.png", "rb") as _f:\n',
    '        import base64 as _b64\n',
    '        _olivia_b64 = _b64.b64encode(_f.read()).decode()\n',
    '    st.markdown(f\'<img src="data:image/png;base64,{_olivia_b64}" style="width:100%;border-radius:16px;margin-bottom:20px;box-shadow:0 4px 20px rgba(0,0,0,0.15);" />\', unsafe_allow_html=True)\n',
    '\n',
]

lines[idx:idx_fim] = novo_header
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
