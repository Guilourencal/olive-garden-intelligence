lines = open('dashboard.py', 'r', encoding='utf-8').read().split('\n')
nova = []
nova.append('elif aba_sel == "OlivIA":')
nova.append('    import base64 as b64')
nova.append('    with open("assets/Olivia_Fundo_Branco_Header.png", "rb") as img_f:')
nova.append('        olivia_img = b64.b64encode(img_f.read()).decode("utf-8")')
nova.append('    st.markdown(')
nova.append('        f"""<div style="background:#3D2B1F; border-radius:16px; overflow:hidden; display:flex; align-items:stretch; min-height:260px; margin-bottom:24px; position:relative;">')
nova.append('        <div style="flex:1; padding:48px 48px 48px 56px; display:flex; flex-direction:column; justify-content:center; position:relative; z-index:1;">')
nova.append('        <div style="font-size:10px; letter-spacing:5px; color:#8B9A2E; text-transform:uppercase; margin-bottom:16px; font-family:Arial,sans-serif;">Agente de inteligencia - Olive Garden Brasil</div>')
nova.append('        <div style="margin-bottom:12px; line-height:1;">')
nova.append('        <span style="font-family:Georgia,serif; font-size:72px; font-weight:800; color:#F5F0E8; letter-spacing:2px;">Oliv</span><span style="font-family:Georgia,serif; font-size:72px; font-weight:800; color:#8B9A2E; letter-spacing:2px;">IA</span>')
nova.append('        </div>')
nova.append('        <div style="width:64px; height:2px; background:#8B9A2E; margin-bottom:20px;"></div>')
nova.append('        <div style="font-size:14px; color:#D8CFC0; line-height:1.8; max-width:400px; font-family:Arial,sans-serif; margin-bottom:28px;">Analiso reviews, redes sociais, pesquisa interna e noticias do mercado para gerar insights estrategicos em tempo real.</div>')
nova.append('        <div style="display:flex; gap:12px; flex-wrap:wrap;">')
nova.append('        <div style="background:rgba(139,154,46,0.15); border:1px solid rgba(139,154,46,0.35); border-radius:10px; padding:10px 18px;"><div style="font-size:10px; color:#8B9A2E; letter-spacing:2px; text-transform:uppercase; font-family:Arial,sans-serif; margin-bottom:2px;">Reviews</div><div style="font-size:18px; font-weight:700; color:#F5F0E8; font-family:Georgia,serif;">{len(df)}</div></div>')
nova.append('        <div style="background:rgba(139,154,46,0.15); border:1px solid rgba(139,154,46,0.35); border-radius:10px; padding:10px 18px;"><div style="font-size:10px; color:#8B9A2E; letter-spacing:2px; text-transform:uppercase; font-family:Arial,sans-serif; margin-bottom:2px;">Filiais</div><div style="font-size:18px; font-weight:700; color:#F5F0E8; font-family:Georgia,serif;">6</div></div>')
nova.append('        <div style="background:rgba(139,154,46,0.15); border:1px solid rgba(139,154,46,0.35); border-radius:10px; padding:10px 18px;"><div style="font-size:10px; color:#8B9A2E; letter-spacing:2px; text-transform:uppercase; font-family:Arial,sans-serif; margin-bottom:2px;">Social</div><div style="font-size:18px; font-weight:700; color:#F5F0E8; font-family:Georgia,serif;">{len(df_social)}</div></div>')
nova.append('        <div style="background:rgba(139,154,46,0.15); border:1px solid rgba(139,154,46,0.35); border-radius:10px; padding:10px 18px;"><div style="font-size:10px; color:#8B9A2E; letter-spacing:2px; text-transform:uppercase; font-family:Arial,sans-serif; margin-bottom:2px;">Powered by</div><div style="font-size:18px; font-weight:700; color:#F5F0E8; font-family:Georgia,serif;">Claude</div></div>')
nova.append('        </div></div>')
nova.append('        <div style="width:280px; flex-shrink:0; display:flex; align-items:flex-end; justify-content:center; overflow:hidden; background:linear-gradient(to right, #3D2B1F, #4A3525);">')
nova.append('        <img src="data:image/png;base64,{olivia_img}" style="height:260px; object-fit:contain; object-position:bottom;"/>')
nova.append('        </div>')
nova.append('        </div>""",')
nova.append('        unsafe_allow_html=True')
nova.append('    )')
for i, line in enumerate(lines):
    if 'elif aba_sel == "OlivIA":' in line:
        start = i
        break
for i, line in enumerate(lines[start+1:], start+1):
    if line.strip().startswith('st.markdown(') and 'unsafe_allow_html=True' in lines[i+2] if i+2 < len(lines) else False:
        end = i + 3
        break
    if 'preparar_contexto' in line:
        end = i
        break
result = lines[:start] + nova + lines[end:]
open('dashboard.py', 'w', encoding='utf-8').write('\n'.join(result))
print('Feito! Linhas:', len(result))
