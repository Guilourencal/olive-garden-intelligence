import base64
from PIL import Image

# Reprocessar imagem com corte mais preciso
img = Image.open('static/olivia.png').convert('RGBA')
w, h = img.size

# Recortar apenas a figura central da versao esquerda (remover bordas com graficos)
# Versao esquerda ocupa primeiro 1/3, mas a figura esta mais ao centro
versao_esq = img.crop((int(w*0.05), int(h*0.05), int(w*0.38), h))

# Remover fundo branco/claro com threshold mais agressivo
data = list(versao_esq.getdata())
new_data = []
for r, g, b, a in data:
    if r > 220 and g > 220 and b > 220:
        new_data.append((r, g, b, 0))
    else:
        new_data.append((r, g, b, a))
versao_esq.putdata(new_data)
versao_esq.save('static/olivia_header.png', 'PNG')

with open('static/olivia_header.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if '_olivia_b64 = "' in l)
lines[idx] = '    _olivia_b64 = "' + img_b64 + '"\n'

# Corrigir altura do header — remover padding excessivo
for i in range(idx, idx+20):
    if 'padding:28px 36px' in lines[i]:
        lines[i] = lines[i].replace('padding:28px 36px', 'padding:20px 32px')
    if 'font-size:44px' in lines[i]:
        lines[i] = lines[i].replace('font-size:44px', 'font-size:36px')
    if 'width:180px' in lines[i]:
        lines[i] = lines[i].replace('width:180px', 'width:160px')
        lines[i] = lines[i].replace('width:180px;height:auto', 'width:160px;height:160px')

open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
