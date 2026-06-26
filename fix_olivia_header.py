content = open('dashboard.py', 'r', encoding='utf-8').read()

old = '''elif aba_sel == "OlivIA":
    st.markdown(\'<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">OlivIA</div>\', unsafe_allow_html=True)
    st.markdown(\'<div style="font-size:13px; color:#8B9A2E; letter-spacing:0.1em; margin-bottom:20px;">ANALISTA DE DADOS VIRTUAL — OLIVE GARDEN BRASIL</div>\', unsafe_allow_html=True)'''

new = '''elif aba_sel == "OlivIA":
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

if old in content:
    content = content.replace(old, new)
    open('dashboard.py', 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('TRECHO NAO ENCONTRADO')
