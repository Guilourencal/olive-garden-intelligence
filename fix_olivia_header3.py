import base64

with open('static/olivia.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

# Encontrar linha do elif OlivIA
idx = next(i for i, l in enumerate(lines) if 'elif aba_sel == "OlivIA":' in l)

# Novo header
novo_header = [
    'elif aba_sel == "OlivIA":\n',
    '    _olivia_b64 = "' + img_b64 + '"\n',
    '    st.markdown(\n',
    '        \'<div style="background:linear-gradient(135deg,#1a3320 0%,#2e5435 100%);border-radius:16px;padding:0;display:flex;align-items:stretch;overflow:hidden;margin-bottom:24px;box-shadow:0 4px 16px rgba(26,51,32,0.18);min-height:160px;">\'\n',
    '        \'<div style="flex:1;padding:32px 36px;display:flex;flex-direction:column;justify-content:center;">\'\n',
    '        \'<div style="font-size:11px;color:#8B9A2E;letter-spacing:0.18em;margin-bottom:10px;text-transform:uppercase;">Agente de Inteligencia · Olive Garden Brasil</div>\'\n',
    '        \'<div style="font-size:38px;font-weight:900;color:#F5F0E8;letter-spacing:0.04em;line-height:1;">Oliv<span style="color:#8B9A2E;">IA</span></div>\'\n',
    '        \'<div style="width:48px;height:3px;background:#8B9A2E;margin:12px 0;border-radius:2px;"></div>\'\n',
    '        \'<div style="font-size:13px;color:#D8CFC0;line-height:1.6;">Dados conectados. Insights claros.<br>Decisoes inteligentes.</div>\'\n',
    '        \'</div>\'\n',
    '        f\'<div style="width:220px;flex-shrink:0;display:flex;align-items:flex-end;justify-content:center;overflow:hidden;"><img src="data:image/png;base64,{_olivia_b64}" style="height:200px;object-fit:contain;object-position:bottom;" /></div>\'\n',
    '        \'</div>\',\n',
    '        unsafe_allow_html=True)\n',
]

# Encontrar fim do header antigo (proximas linhas ate importar anthropic)
idx_fim = next(i for i in range(idx, idx+10) if 'import anthropic' in lines[i])

lines[idx:idx_fim] = novo_header
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print(f'OK — header substituido na linha {idx+1}')
