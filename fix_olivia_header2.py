import base64

with open('static/olivia.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''elif aba_sel == "OlivIA":
    st.markdown(\'\'\'
    <div style="background:linear-gradient(135deg,#1a3320 0%,#2e5435 100%);border-radius:16px;padding:24px 28px;display:flex;align-items:center;gap:20px;margin-bottom:24px;box-shadow:0 4px 16px rgba(26,51,32,0.18);">
        <div style="width:64px;height:64px;background:#8B9A2E;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;flex-shrink:0;box-shadow:0 2px 8px rgba(0,0,0,0.2);">🫒</div>
        <div>
            <div style="font-size:22px;font-weight:800;color:#F5F0E8;letter-spacing:0.06em;">OlivIA</div>
            <div style="font-size:12px;color:#9DC88D;letter-spacing:0.12em;margin-top:2px;">ANALISTA DE DADOS VIRTUAL · OLIVE GARDEN BRASIL</div>
            <div style="font-size:11px;color:#D8CFC0;margin-top:6px;">Faça perguntas sobre vendas, iFood, reviews, pesquisa, fila e menu.</div>
        </div>
    </div>
    \'\'\', unsafe_allow_html=True)'''

new = f\'\'\'elif aba_sel == "OlivIA":
    _olivia_img = "{img_b64}"
    st.markdown(f\'\'\'\'
    <div style="background:linear-gradient(135deg,#1a3320 0%,#2e5435 100%);border-radius:16px;padding:0;display:flex;align-items:stretch;overflow:hidden;margin-bottom:24px;box-shadow:0 4px 16px rgba(26,51,32,0.18);min-height:160px;">
        <div style="flex:1;padding:32px 36px;display:flex;flex-direction:column;justify-content:center;">
            <div style="font-size:11px;color:#8B9A2E;letter-spacing:0.18em;margin-bottom:10px;text-transform:uppercase;">Agente de Inteligencia · Olive Garden Brasil</div>
            <div style="font-size:38px;font-weight:900;color:#F5F0E8;letter-spacing:0.04em;line-height:1;">Oliv<span style="color:#8B9A2E;">IA</span></div>
            <div style="width:48px;height:3px;background:#8B9A2E;margin:12px 0;border-radius:2px;"></div>
            <div style="font-size:13px;color:#D8CFC0;line-height:1.6;">Dados conectados. Insights claros.<br>Decisoes inteligentes.</div>
        </div>
        <div style="width:220px;flex-shrink:0;display:flex;align-items:flex-end;justify-content:center;overflow:hidden;">
            <img src="data:image/png;base64,{{_olivia_img}}" style="height:200px;object-fit:contain;object-position:bottom;" />
        </div>
    </div>
    \'\'\', unsafe_allow_html=True)\'\'\'

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
