lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if 'elif aba_sel == "OlivIA":' in line:
        start = i
        break
for i, line in enumerate(lines[start:], start):
    if 'preparar_contexto' in line:
        end = i
        break
nova = []
nova.append('elif aba_sel == "OlivIA":')
nova.append('    import base64 as b64')
nova.append('    with open("assets/Olivia_Fundo_Branco_Header.png", "rb") as img_f:')
nova.append('        olivia_img = b64.b64encode(img_f.read()).decode("utf-8")')
nova.append('    st.markdown(')
nova.append('        f"""<div style="background:#3D2B1F; border-radius:16px; overflow:hidden; display:flex; align-items:stretch; min-height:280px; margin-bottom:24px;">')
nova.append('        <div style="flex:1; padding:52px 40px 52px 56px; display:flex; flex-direction:column; justify-content:center;">')
nova.append('        <div style="font-size:10px; letter-spacing:5px; color:#8B9A2E; text-transform:uppercase; margin-bottom:16px; font-family:Arial,sans-serif;">Agente de inteligencia - Olive Garden Brasil</div>')
nova.append('        <div style="margin-bottom:12px; line-height:1;">')
nova.append('        <span style="font-family:Georgia,serif; font-size:72px; font-weight:800; color:#F5F0E8; letter-spacing:2px;">Oliv</span><span style="font-family:Georgia,serif; font-size:72px; font-weight:800; color:#8B9A2E; letter-spacing:2px;">IA</span>')
nova.append('        </div>')
nova.append('        <div style="width:64px; height:2px; background:#8B9A2E; margin-bottom:20px;"></div>')
nova.append('        <div style="font-size:14px; color:#D8CFC0; line-height:1.8; max-width:420px; font-family:Arial,sans-serif;">Analiso reviews, redes sociais, pesquisa interna e noticias do mercado para gerar insights estrategicos em tempo real.</div>')
nova.append('        </div>')
nova.append('        <div style="width:320px; flex-shrink:0; display:flex; align-items:flex-end; justify-content:center; overflow:hidden;">')
nova.append('        <img src="data:image/png;base64,{olivia_img}" style="height:300px; object-fit:contain; object-position:bottom; margin-bottom:-4px;"/>')
nova.append('        </div>')
nova.append('        </div>""",')
nova.append('        unsafe_allow_html=True')
nova.append('    )')
result = lines[:start] + nova + lines[end:]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result))
print('Feito! Linhas:', len(result))
