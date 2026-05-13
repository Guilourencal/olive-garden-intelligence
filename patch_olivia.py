with open('dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '    for aba in ["Reviews", "Social", "Notícias", "Pesquisa", "Vendas", "Insights IA"]:'
new = '    for aba in ["Reviews", "Social", "Notícias", "Pesquisa", "Vendas", "Insights IA", "OlivIA"]:'
content = content.replace(old, new)

olivia_block = '''
elif aba_sel == "OlivIA":
    import base64 as b64
    with open("assets/Olivia_Fundo_Branco_Header.png", "rb") as img_f:
        olivia_img = b64.b64encode(img_f.read()).decode("utf-8")
    st.markdown(
        f"""<div style="background:#3D2B1F; border-radius:16px; overflow:hidden; display:flex; align-items:stretch; min-height:280px; margin-bottom:24px;">
        <div style="flex:1; padding:52px 40px 52px 56px; display:flex; flex-direction:column; justify-content:center;">
        <div style="font-size:10px; letter-spacing:5px; color:#8B9A2E; text-transform:uppercase; margin-bottom:16px; font-family:Arial,sans-serif;">Agente de inteligencia - Olive Garden Brasil</div>
        <div style="margin-bottom:12px; line-height:1;">
        <span style="font-family:Georgia,serif; font-size:72px; font-weight:800; letter-spacing:2px; color:#F5F0E8;">Olv<span style="color:#8B9A2E;">ia</span></span>
        </div>
        <div style="width:64px; height:2px; background:#8B9A2E; margin-bottom:20px;"></div>
        <div style="font-size:14px; color:#D8CFC0; line-height:1.8; max-width:420px; font-family:Arial,sans-serif;">Analiso reviews, redes sociais, pesquisa interna e noticias do mercado para gerar insights estrategicos em tempo real.</div>
        </div>
        <div style="width:320px; flex-shrink:0; display:flex; align-items:flex-end; justify-content:center; overflow:hidden;">
        <img src="data:image/png;base64,{olivia_img}" style="height:300px; object-fit:contain; object-position:bottom; margin-bottom:-4px;"/>
        </div>
        </div>""",
        unsafe_allow_html=True
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    client_ai = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        if st.button("Gerar Briefing Executivo", use_container_width=True, key="btn_briefing"):
            with st.spinner("OlivIA esta analisando os dados..."):
                contexto = preparar_contexto()
                response = client_ai.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": f"{contexto}\\n\\nGere um briefing executivo completo sobre a saude da marca Olive Garden Brasil com destaques, pontos de atencao e recomendacoes prioritarias."}]
                )
                st.session_state.chat_history = [{"role": "assistant", "content": response.content[0].text}]
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f\'<div style="background:#e8ddc8; border-radius:10px; padding:12px 16px; margin-bottom:8px; text-align:right;">\' +
                f\'<div style="font-size:13px; color:#3D2B1F;">{msg["content"]}</div></div>\',
                unsafe_allow_html=True
            )
        else:
            with st.container(border=True):
                st.markdown(f\'<div style="font-size:13px; line-height:1.7; color:#3D2B1F;">{msg["content"]}</div>\', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(\'<div class="section-title">Pergunte à OlivIA</div>\', unsafe_allow_html=True)
        pergunta = st.text_input("", placeholder="Digite sua pergunta sobre os dados do Olive Garden Brasil...", key="pergunta_ia", label_visibility="collapsed")
        if st.button("Enviar", key="btn_enviar"):
            if pergunta:
                st.session_state.chat_history.append({"role": "user", "content": pergunta})
                with st.spinner("Analisando..."):
                    contexto = preparar_contexto()
                    mensagens = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                    response = client_ai.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1000,
                        system=contexto,
                        messages=mensagens
                    )
                    st.session_state.chat_history.append({"role": "assistant", "content": response.content[0].text})
                st.rerun()
        if st.button("Limpar conversa", key="btn_limpar"):
            st.session_state.chat_history = []
            st.rerun()

'''

content = content.rstrip()
content += '\n' + olivia_block

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
