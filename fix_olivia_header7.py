import base64
with open('static/olivia_header.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if 'elif aba_sel == "OlivIA":' in l)
idx_fim = next(i for i in range(idx, idx+25) if '# Inicializar historico' in lines[i])

novo_header = [
    'elif aba_sel == "OlivIA":\n',
    '    import anthropic as _anthropic\n',
    '    import json as _json\n',
    '    _olivia_b64 = "' + img_b64 + '"\n',
    '    st.markdown(f\'\'\'<div style="background:linear-gradient(135deg,#1a3320 0%,#2e5435 100%);border-radius:16px;padding:28px 36px;display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;box-shadow:0 4px 20px rgba(0,0,0,0.15);">\n',
    '        <div style="flex:1;">\n',
    '            <div style="font-size:10px;color:#8B9A2E;letter-spacing:0.2em;margin-bottom:10px;text-transform:uppercase;">Agente de Inteligencia · Olive Garden Brasil</div>\n',
    '            <div style="font-size:44px;font-weight:900;color:#F5F0E8;line-height:1;">Oliv<span style="color:#8B9A2E;">IA</span></div>\n',
    '            <div style="width:50px;height:3px;background:#8B9A2E;margin:12px 0;border-radius:2px;"></div>\n',
    '            <div style="font-size:13px;color:#D8CFC0;line-height:1.8;">Dados conectados. Insights claros.<br>Decisoes inteligentes.</div>\n',
    '        </div>\n',
    '        <div style="width:180px;display:flex;align-items:flex-end;justify-content:flex-end;flex-shrink:0;">\n',
    '            <img src="data:image/png;base64,{_olivia_b64}" style="width:180px;height:auto;object-fit:contain;filter:drop-shadow(0 4px 16px rgba(0,0,0,0.4));" />\n',
    '        </div>\n',
    '    </div>\'\'\', unsafe_allow_html=True)\n',
    '\n',
]

lines[idx:idx_fim] = novo_header
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
