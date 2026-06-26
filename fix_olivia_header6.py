import base64

with open('static/olivia_header.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if 'elif aba_sel == "OlivIA":' in l)
idx_fim = next(i for i in range(idx, idx+20) if 'import anthropic' in lines[i])

novo_header = [
    'elif aba_sel == "OlivIA":\n',
    '    import anthropic as _anthropic\n',
    '    import json as _json\n',
    '\n',
    '    # Header com colunas Streamlit\n',
    '    _olivia_b64 = "' + img_b64 + '"\n',
    '    col_txt, col_img = st.columns([3, 1])\n',
    '    with col_txt:\n',
    '        st.markdown(\'\'\'\n',
    '        <div style="background:linear-gradient(135deg,#1a3320 0%,#2e5435 100%);border-radius:16px 0 0 16px;padding:32px 40px;height:100%;min-height:160px;">\n',
    '            <div style="font-size:10px;color:#8B9A2E;letter-spacing:0.2em;margin-bottom:12px;text-transform:uppercase;">Agente de Inteligencia · Olive Garden Brasil</div>\n',
    '            <div style="font-size:42px;font-weight:900;color:#F5F0E8;line-height:1;font-family:Nunito,sans-serif;">Oliv<span style="color:#8B9A2E;">IA</span></div>\n',
    '            <div style="width:52px;height:3px;background:#8B9A2E;margin:14px 0 10px 0;border-radius:2px;"></div>\n',
    '            <div style="font-size:13px;color:#D8CFC0;line-height:1.7;">Dados conectados. Insights claros.<br>Decisoes inteligentes.</div>\n',
    '        </div>\n',
    '        \'\'\', unsafe_allow_html=True)\n',
    '    with col_img:\n',
    '        st.markdown(f\'<div style="background:linear-gradient(135deg,#1a3320 0%,#2e5435 100%);border-radius:0 16px 16px 0;display:flex;align-items:flex-end;justify-content:center;height:100%;min-height:160px;overflow:hidden;"><img src="data:image/png;base64,{_olivia_b64}" style="max-height:200px;width:auto;object-fit:contain;object-position:bottom;" /></div>\', unsafe_allow_html=True)\n',
    '\n',
]

lines[idx:idx_fim] = novo_header
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
