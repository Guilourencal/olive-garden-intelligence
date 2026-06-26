lines = open('dashboard.py', 'r', encoding='utf-8').readlines()

novo_olivia = '''elif aba_sel == "OlivIA":
    st.markdown(\'<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">OlivIA</div>\', unsafe_allow_html=True)
    st.markdown(\'<div style="font-size:13px; color:#8B9A2E; letter-spacing:0.1em; margin-bottom:20px;">ANALISTA DE DADOS VIRTUAL — OLIVE GARDEN BRASIL</div>\', unsafe_allow_html=True)

    import anthropic as _anthropic
from db import get_conn
    import json as _json

    # Inicializar historico na sessao
    if "olivia_messages" not in st.session_state:
        st.session_state.olivia_messages = []

    # System prompt com schema completo do banco
    OLIVIA_SYSTEM = """Voce e a OlivIA, analista de dados virtual do Olive Garden Brasil.
Voce tem acesso ao banco de dados PostgreSQL (Supabase) com as seguintes tabelas:

1. vendas_diarias — colunas: data, filial, ano, mes, venda_salao, meta_venda, venda_ano1, gc_salao, ticket_total, hdc, venda_por_hdc
   Filiais: Olive Garden - Morumbi, Olive Garden - Center Norte, Olive Garden - Dom Pedro, Olive Garden - Aricanduva, Olive Garden - Guarulhos GRU2, Olive Garden - Guarulhos GRU3
   Siglas: MOR=Morumbi, CNO=Center Norte, DPO=Dom Pedro, ARI=Aricanduva, GRU2=Guarulhos GRU2, GRU3=Guarulhos GRU3

2. ifood_vendas — colunas: periodo, filial, logistica, pedidos, faturamento, taxa_entrega, ticket_medio, novos_clientes
   Apenas 4 filiais tem iFood: Morumbi, Center Norte, Dom Pedro, Aricanduva

3. ifood_diario — colunas: data, filial, pedidos, faturamento, taxa_entrega, ticket_medio, novos_clientes
   Dados diarios do iFood do mes corrente

4. reclamacoes_buzzmonitor — colunas: data, comentario, canal, sentimento, avaliacao, unidade, unidade_curta, tema, subtema
   Canal: google_my_business ou instagram. Periodo: jan-jun 2026

5. reviews — colunas: filial, plataforma, nota, sentimento, texto, data
   Plataformas: iFood (761 reviews, nota 4.8), Google Reviews (30), TripAdvisor (113)

6. pesquisa_performance — colunas: periodo, restaurant, overall_experience, value, service, taste, speed_of_service, clean, soup_salad_refill, breadstick_refill
   Metricas em percentual (0-100)

7. pesquisa_comments — colunas: survey_date, filial, overall_rating, verbatim, period
   overall_rating: Highly Satisfied, Satisfied, Dissatisfied, Highly Dissatisfied

8. fila_espera — colunas: dia_chegada, hora_chegada, pessoas, duracao_minutos, status, unidade
   Status: Sentado, Cancelado por solicitacao do cliente, Cancelado pelo cliente, Cancelado por no-show do cliente

9. menu_analysis — colunas: semana_ref, item, type, number_of_checks, gross_sales, ct_gross_total_check_avg, check_uplift, revenue_score
   type (Boston): Star, Plow Horse, Puzzle, Dog

10. projecoes_historico — colunas: data_alvo, filial, valor_projetado, valor_realizado, erro_pct
    Projecoes de vendas dos proximos 28 dias

11. calendario_eventos — colunas: data_inicio, data_fim, filial, nome_evento, tipo, observacao

Regras:
- Responda SEMPRE em portugues brasileiro
- Para perguntas sobre dados, gere uma query SQL e apresente os resultados em tabela markdown + analise
- Use linguagem executiva, direta e objetiva
- Quando nao souber, diga claramente
- Nunca execute UPDATE, DELETE, DROP ou INSERT — apenas SELECT
- Contexto atual: junho 2026, Copa do Mundo em andamento, rede com 6 filiais em SP

Formato da resposta:
1. Breve introducao (1 linha)
2. Tabela com os dados (markdown)
3. Analise executiva (3-5 bullets com insights)
"""

    # Conexao ao banco para execucao de queries
    def _executar_query(sql):
        try:
            import psycopg2
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(sql)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return cols, rows
        except Exception as e:
            return None, str(e)

    # Exibir historico
    for msg in st.session_state.olivia_messages:
        with st.chat_message(msg["role"], avatar="🫒" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    # Input do usuario
    pergunta = st.chat_input("Faça uma pergunta sobre os dados do Olive Garden...")

    if pergunta:
        # Adicionar pergunta ao historico
        st.session_state.olivia_messages.append({"role": "user", "content": pergunta})
        with st.chat_message("user", avatar="👤"):
            st.markdown(pergunta)

        with st.chat_message("assistant", avatar="🫒"):
            with st.spinner("OlivIA analisando..."):
                try:
                    client = _anthropic.Anthropic()

                    # Montar historico para o LLM
                    messages_llm = []
                    for m in st.session_state.olivia_messages[:-1]:
                        messages_llm.append({"role": m["role"], "content": m["content"]})

                    # Primeira chamada — gerar SQL
                    messages_llm.append({
                        "role": "user",
                        "content": f"""{pergunta}

Se precisar de dados do banco, responda PRIMEIRO com um bloco SQL assim:
`sql
SELECT ...
`
Depois apresente a analise. Se nao precisar de SQL, responda diretamente."""
                    })

                    resp1 = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=2000,
                        system=OLIVIA_SYSTEM,
                        messages=messages_llm
                    )
                    resposta1 = resp1.content[0].text

                    # Verificar se tem SQL
                    resposta_final = resposta1
                    if "`sql" in resposta1.lower():
                        import re as _re
                        sql_match = _re.search(r"`sql\s*(.*?)\s*`", resposta1, _re.DOTALL | _re.IGNORECASE)
                        if sql_match:
                            sql = sql_match.group(1).strip()
                            # Seguranca — apenas SELECT
                            sql_upper = sql.upper().strip()
                            if any(sql_upper.startswith(w) for w in ["UPDATE","DELETE","DROP","INSERT","ALTER","TRUNCATE"]):
                                resposta_final = "Nao posso executar operacoes de escrita no banco."
                            else:
                                cols, rows = _executar_query(sql)
                                if cols and isinstance(rows, list):
                                    # Montar tabela markdown
                                    tabela = "| " + " | ".join(cols) + " |\n"
                                    tabela += "| " + " | ".join(["---"]*len(cols)) + " |\n"
                                    for row in rows[:50]:
                                        tabela += "| " + " | ".join([str(v) if v is not None else "—" for v in row]) + " |\n"

                                    # Segunda chamada — analise com os dados
                                    messages_llm2 = messages_llm + [
                                        {"role": "assistant", "content": resposta1},
                                        {"role": "user", "content": f"Aqui estao os dados retornados pelo banco:\n\n{tabela}\n\nAgora apresente a analise executiva completa com a tabela e insights."}
                                    ]
                                    resp2 = client.messages.create(
                                        model="claude-sonnet-4-6",
                                        max_tokens=2000,
                                        system=OLIVIA_SYSTEM,
                                        messages=messages_llm2
                                    )
                                    resposta_final = resp2.content[0].text
                                else:
                                    resposta_final = f"Erro ao consultar o banco: {rows}"

                    st.markdown(resposta_final)
                    st.session_state.olivia_messages.append({"role": "assistant", "content": resposta_final})

                except Exception as e:
                    erro = f"Erro na OlivIA: {str(e)}"
                    st.error(erro)
                    st.session_state.olivia_messages.append({"role": "assistant", "content": erro})

    # Botao limpar historico
    if st.session_state.olivia_messages:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Limpar conversa", key="limpar_olivia"):
            st.session_state.olivia_messages = []
            st.rerun()

'''

lines[1657:1915] = [novo_olivia]
open('dashboard.py', 'w', encoding='utf-8').write(''.join(lines))
print(f'OK — {len(lines)} linhas')
