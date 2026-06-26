import base64

with open('static/Olivia_Header_Novo.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

lines = open('dashboard.py', 'r', encoding='utf-8').readlines()
idx = next(i for i, l in enumerate(lines) if 'with open("static/olivia_banner.png"' in l)
lines[idx] = '    with open("static/Olivia_Header_Novo.png", "rb") as _f:\n'
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print('OK')
