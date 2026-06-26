import base64

# Ler imagem atual e reprocessar localmente
from PIL import Image
import io

img = Image.open('static/olivia.png').convert('RGBA')
w, h = img.size
# Recortar versao esquerda (1/3 da imagem)
versao_esq = img.crop((0, 0, w//3, h))

# Remover fundo branco
data = list(versao_esq.getdata())
new_data = []
for r, g, b, a in data:
    if r > 230 and g > 230 and b > 230:
        new_data.append((r, g, b, 0))
    else:
        new_data.append((r, g, b, a))
versao_esq.putdata(new_data)
versao_esq.save('static/olivia_header.png', 'PNG')

with open('static/olivia_header.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if 'elif aba_sel == "OlivIA":' in l)
idx_fim = next(i for i in range(idx, idx+20) if 'import anthropic' in lines[i])

novo_header = [
    'elif aba_sel == "OlivIA":\n',
    '    _olivia_b64 = "' + img_b64 + '"\n',
    '    st.markdown(\n',
    '        \'<div style="background:linear-gradient(135deg,#1a3320 0%,#2e5435 100%);border-radius:16px;display:flex;align-items:stretch;overflow:hidden;margin-bottom:24px;box-shadow:0 4px 16px rgba(26,51,32,0.18);min-height:170px;">\'\n',
    '        \'<div style="flex:1;padding:32px 40px;display:flex;flex-direction:column;justify-content:center;">\'\n',
    '        \'<div style="font-size:10px;color:#8B9A2E;letter-spacing:0.2em;margin-bottom:12px;text-transform:uppercase;">Agente de Inteligencia · Olive Garden Brasil</div>\'\n',
    '        \'<div style="font-size:42px;font-weight:900;color:#F5F0E8;letter-spacing:0.02em;line-height:1;font-family:Nunito,sans-serif;">Oliv<span style="color:#8B9A2E;">IA</span></div>\'\n',
    '        \'<div style="width:52px;height:3px;background:#8B9A2E;margin:14px 0 10px 0;border-radius:2px;"></div>\'\n',
    '        \'<div style="font-size:13px;color:#D8CFC0;line-height:1.7;font-style:italic;">Dados conectados. Insights claros.<br>Decisoes inteligentes.</div>\'\n',
    '        \'</div>\'\n',
    '        + f\'<div style="width:240px;flex-shrink:0;display:flex;align-items:flex-end;justify-content:flex-end;padding-right:0;overflow:hidden;"><img src="data:image/png;base64,{_olivia_b64}" style="height:210px;object-fit:contain;object-position:bottom right;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.3));" /></div>\'\n',
    '        + \'</div>\',\n',
    '        unsafe_allow_html=True)\n',
    '\n',
]

lines[idx:idx_fim] = novo_header
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
