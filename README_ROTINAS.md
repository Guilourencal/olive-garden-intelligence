# ROTINAS OPERACIONAIS — OLIVE GARDEN BRAND INTELLIGENCE

## ATUALIZACOES DIARIAS

### 1. Atualizar Vendas — Operacao Geral (Salao)
Executar quando receber o arquivo DASH VENDAS atualizado.

`powershell
copy "C:\olive-garden-reviews\data\Vendas_Geral\NOME_DO_ARQUIVO.xlsx" "C:\olive-garden-reviews\data\dash_vendas.xlsx"
python reimportar_vendas_diarias.py
python aprender_modelo.py
`

**Importante:** substituir NOME_DO_ARQUIVO pelo nome real do arquivo recebido.
O script aprender_modelo.py deve ser rodado APOS confirmar que o reimport foi bem-sucedido.

---

### 2. Atualizar Vendas iFood
Executar quando receber o arquivo iFood_Vendas atualizado.

`powershell
python importar_ifood_vendas.py
`

**Observacao:** o script limpa automaticamente o periodo parcial anterior antes de importar o novo.
Os arquivos devem estar em: C:\olive-garden-reviews\data\ifood_vendas\

---

### 3. Atualizar Pesquisa GSS
Executar quando receber novos arquivos Brazil FW e Brazil OG Comments.

`powershell
copy "CAMINHO_ORIGEM\Brazil FW*.xlsx" "C:\olive-garden-reviews\data\"
copy "CAMINHO_ORIGEM\Brazil OG Comments*.xlsx" "C:\olive-garden-reviews\data\"
python importar_pesquisa.py
`

---

### 4. Atualizacao Automatica (Task Scheduler — 9h)
Roda automaticamente todo dia as 9h via Windows Task Scheduler.
Atualiza: Google Reviews, noticias, sentimento, banco Supabase.

`powershell
python atualizar_tudo.py
`

**Observacao:** conexao ao Supabase so funciona pelo hotspot do celular.

---

## SISTEMA DE APRENDIZADO CONTINUO

O script prender_modelo.py executa 3 etapas:

1. **Calcula erros passados** — compara projecoes anteriores com o realizado
2. **Registra novas projecoes** — salva projecoes dos proximos 28 dias no banco
3. **Recalibra parametros** — atualiza MAPE e bias por filial

Os dados ficam na tabela projecoes_historico e modelo_parametros no Supabase.
Com o tempo, o modelo se torna cada vez mais preciso por filial.

---

## RESTAURAR VERSAO ESTAVEL

Em caso de erro grave no dashboard.py:

`powershell
# Restaurar ultimo commit
git checkout HEAD -- dashboard.py

# Restaurar versao estavel 18/05/2026
git checkout v-estavel-20260518 -- dashboard.py
`

---

## BANCO DE DADOS SUPABASE

| Tabela | Conteudo | Script de atualizacao |
|---|---|---|
| vendas_diarias | 502 dias x 6 filiais | reimportar_vendas_diarias.py |
| ifood_vendas | vendas iFood por periodo | importar_ifood_vendas.py |
| pesquisa_performance | GSS topbox por filial | importar_pesquisa.py |
| pesquisa_comments | comentarios internos | importar_pesquisa.py |
| reviews | Google + TripAdvisor + iFood | atualizar_tudo.py |
| social | comentarios Instagram | atualizar_tudo.py |
| projecoes_historico | historico de projecoes | aprender_modelo.py |
| modelo_parametros | parametros calibrados | aprender_modelo.py |

---

## CREDENCIAIS

- Dashboard: https://olive-garden-intelligence-y6fxcw4xtblkyca3tsha8g.streamlit.app/
- Senha: olivegarden2026
- Repositorio: https://github.com/Guilourencal/olive-garden-intelligence
- Supabase: aws-1-sa-east-1.pooler.supabase.com:6543

---

*Ultima atualizacao: 19/05/2026*
