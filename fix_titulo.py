content = open('dashboard.py', 'r', encoding='utf-8').read()
old = '<span style="font-family:Georgia,serif; font-size:72px; font-weight:800; color:#F5F0E8; letter-spacing:2px;">Oliv</span><span style="font-family:Georgia,serif; font-size:72px; font-weight:800; color:#8B9A2E; letter-spacing:2px;">IA</span>'
new = '<span style="font-family:Georgia,serif; font-size:72px; font-weight:800; letter-spacing:2px;"><span style="color:#F5F0E8;">Oliv</span><span style="color:#8B9A2E;">IA</span></span>'
if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('Feito!')
else:
    print('Trecho nao encontrado')
