import streamlit as st
from db import get_conn, get_conn_ro
import os
from dotenv import load_dotenv
load_dotenv()

def verificar_senha():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if not st.session_state.autenticado:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown('<div style="text-align:center; font-size:11px; letter-spacing:0.2em; color:#8B9A2E; text-transform:uppercase; margin-bottom:16px;">Brand Intelligence</div>', unsafe_allow_html=True)
            senha = st.text_input("Senha de acesso", type="password", key="senha_input")
            if st.button("Entrar", use_container_width=True):
                if senha == os.getenv("DASHBOARD_PASSWORD"):
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta")
        st.stop()

import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import re
import os
import numpy as np
from datetime import datetime, timedelta
import anthropic

st.set_page_config(
    page_title="Olive Garden — Brand Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_b64 = get_base64_image("assets/logo_og.png")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&display=swap');
* { font-family: 'Nunito', sans-serif; }
[data-testid="stAppViewContainer"] { background-color: #F5F0E8; }
/* ── SIDEBAR BASE ── */
[data-testid="stSidebar"] { background-color: #3D2710; border-right: 2px solid rgba(139,154,46,0.35); }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: #C8BFB0 !important; }
/* ── BOTÕES DE NAVEGAÇÃO ── */
[data-testid="stSidebar"] button {
  border-radius: 6px !important;
  border: none !important;
  background: transparent !important;
  color: #A89880 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  padding: 7px 12px !important;
  margin-bottom: 1px !important;
  transition: all 0.15s ease !important;
  border-left: 2px solid transparent !important;
}
[data-testid="stSidebar"] button:hover {
  background: rgba(139,154,46,0.12) !important;
  color: #C8D870 !important;
  border-left: 2px solid #8B9A2E !important;
}
/* ── SELECTBOX ── */
[data-testid="stSidebar"] .stSelectbox > div > div {
  background-color: rgba(255,255,255,0.05) !important;
  color: #E8DCC8 !important;
  border: none !important;
  border-bottom: 1px solid rgba(139,154,46,0.4) !important;
  border-radius: 0 !important;
  font-size: 12px !important;
  padding: 6px 8px !important;
}
[data-baseweb="select"] [data-baseweb="popover"] ul { max-height: 400px !important; overflow-y: auto !important; }
[data-baseweb="popover"] { z-index: 9999 !important; }
/* ── ABA ATIVA ── */
.nav-ativo { background:rgba(139,154,46,0.15); border-left:3px solid #8B9A2E !important;
  border-radius:6px; padding:7px 12px; margin-bottom:1px;
  font-size:11px; font-weight:800; letter-spacing:0.1em;
  text-transform:uppercase; color:#8B9A2E; display:block; }
/* ── SIDEBAR LABEL ── */
.sidebar-label { font-size:9px; letter-spacing:0.18em; text-transform:uppercase;
  color:rgba(139,154,46,0.7); margin:14px 0 3px; font-weight:700; }
[data-testid="stMetricLabel"] { font-size: 11px !important; letter-spacing: 0.1em; text-transform: uppercase; color: #5C3D1E !important; }
[data-testid="stMetricValue"] { font-weight: 800 !important; font-size: 28px !important; color: #3D2B1F !important; }
[data-testid="metric-container"] { background: white; border-radius: 12px; padding: 20px; border-bottom: 3px solid #8B9A2E; box-shadow: 0 2px 8px rgba(61,43,31,0.08); }
.section-title { font-weight: 800; font-size: 13px; letter-spacing: 0.15em; text-transform: uppercase; color: #8B9A2E; margin-bottom: 12px; }
.sidebar-label { font-size: 10px; letter-spacing: 0.15em; text-transform: uppercase; color: #8B9A2E; margin-bottom: 4px; }
.indice-card { background: white; border-radius: 12px; padding: 24px; text-align: center; border-bottom: 4px solid #8B9A2E; box-shadow: 0 2px 8px rgba(61,43,31,0.08); height: 100%; }
.indice-valor { font-size: 56px; font-weight: 800; line-height: 1; }
.indice-label { font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; color: #8B9A2E; margin-top: 8px; }
.indice-sub { font-size: 12px; color: #7a5c3a; margin-top: 4px; }
.ranking-row { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e8ddc8; }
.ranking-row:last-child { border-bottom: none; }
.ranking-pos { font-size: 18px; font-weight: 800; color: #8B9A2E; width: 28px; }
.ranking-nome { font-size: 13px; color: #3D2B1F; font-weight: 600; flex: 1; padding: 0 12px; }
.ranking-badge { font-size: 11px; padding: 3px 10px; border-radius: 10px; font-weight: 700; }
.badge-green { background: #e8f2eb; color: #2e6b3e; }
.badge-yellow { background: #f5f0df; color: #7a5c1a; }
.badge-red { background: #f5e8e8; color: #7a2424; }
.ranking-nota { font-size: 15px; font-weight: 800; color: #3D2B1F; width: 40px; text-align: right; }
.comment-card { background: white; border-radius: 10px; padding: 14px; margin-bottom: 10px; border-left: 4px solid #8B9A2E; box-shadow: 0 1px 4px rgba(61,43,31,0.06); }
.comment-card.neg { border-left-color: #8B2E2E; }
.comment-autor { font-size: 12px; font-weight: 700; color: #3D2B1F; }
.comment-texto { font-size: 13px; color: #5C3D1E; margin-top: 4px; line-height: 1.5; }
.comment-meta { font-size: 10px; color: #b0a090; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)

MARROM = "#3D2B1F"
VERDE = "#8B9A2E"
BEGE = "#D8CFC0"
VERMELHO = "#8B2E2E"
CORES_SENT = {"Positivo": VERDE, "Negativo": VERMELHO, "Neutro": "#B8923A"}

STOPWORDS_PT = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "uma",
    "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "ao",
    "ele", "das", "seu", "sua", "ou", "quando", "muito", "nos", "ja", "eu",
    "tambem", "so", "pelo", "pela", "ate", "isso", "ela", "entre", "depois",
    "sem", "mesmo", "aos", "seus", "quem", "nas", "me", "esse", "eles", "voce",
    "essa", "num", "nem", "suas", "meu", "minha", "numa", "pelos", "elas",
    "qual", "nos", "lhe", "deles", "essas", "esses", "pelas", "este", "dele",
    "tu", "te", "voces", "vos", "lhes", "meus", "minhas", "teu", "tua", "teus",
    "tuas", "nosso", "nossa", "nossos", "nossas", "foi", "sao", "esta", "tem",
    "havia", "ser", "ter", "ha", "nao", "sim", "pois", "entao", "porque",
    "quando", "onde", "aqui", "ali", "la", "assim", "tudo", "nada", "algo",
    "alguem", "nenhum", "todo", "toda", "todos", "todas", "outro", "outra",
    "outros", "outras", "pouco", "menos", "pedimos", "bem", "mal", "ainda", "sempre",
    "nunca", "talvez", "apenas", "porem", "contudo", "todavia", "entretanto",
    "logo", "portanto", "the", "and", "was", "for", "this", "with", "but",
    "are", "have", "had", "restaurant", "restaurante", "olive", "garden",
    "fui", "vez", "faz", "estava", "estavam", "tinha", "tinham", "veio",
    "vieram", "ficou", "ficaram", "fazer", "feito", "disse", "disseram",
    "falou", "falaram", "coisa", "coisas", "lugar", "lugares", "parte",
    "hora", "horas", "dia", "dias", "ano", "anos", "mes", "meses", "gente",
    "pessoa", "pessoas", "fica", "ficam", "vem", "vai", "viemos", "fizer",
    "fizeram", "fizemos", "precisa", "precisamos", "precisei", "preciso",
    "deu", "deram", "dava", "pode", "podem", "podemos", "consegui",
    "conseguiu", "conseguimos", "fomos", "foram", "somos", "estou", "estamos",
    "estive", "tive", "tivemos", "tiveram", "queria", "quero", "queremos",
    "sendo", "tendo", "estando", "neste", "nesta", "nesse", "nessa", "aquele",
    "aquela", "aquilo", "tanto", "quanto", "bastante", "demais", "qualquer",
    "cada", "certo", "certa", "varios", "varias", "algum", "alguma", "alguns",
    "algumas", "nenhuma", "since", "been", "they", "their", "there", "what",
    "when", "which", "will", "would", "could", "should", "that", "from",
    "not", "all", "one", "two", "its", "our", "your", "more", "very", "also",
    "after", "about", "just", "like", "time", "really", "came", "said",
    "went", "come", "good", "great", "place", "food", "service", "told",
    "back", "well", "even", "never", "always", "got", "duas", "vontade", "principal", "porém",
    "recomendo",
}

@st.cache_data(ttl=300)
def carregar_reviews():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM reviews", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_social():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM social", conn)
    conn.close()
    return df

@st.cache_data(ttl=1)
def carregar_noticias():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM noticias ORDER BY publicado_em DESC", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_pesquisa_comments():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM pesquisa_comments ORDER BY survey_date DESC", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_pesquisa_performance():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM pesquisa_performance", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_ifood_vendas():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ifood_vendas ORDER BY periodo, filial", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_ifood_horarios():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ifood_horarios", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_ifood_pagamentos():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ifood_pagamentos", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_ifood_dias():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ifood_dias", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_ifood_tags():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ifood_tags ORDER BY periodo, filial, tipo, tag", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_menu_analysis():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM menu_analysis ORDER BY semana_ref DESC, gross_sales DESC", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_ifood_diario():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM ifood_diario ORDER BY data", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_fila_espera():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM fila_espera ORDER BY dia_chegada DESC, hora_chegada DESC", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def carregar_reclamacoes():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM reclamacoes_buzzmonitor ORDER BY data DESC", conn)
    conn.close()
    return df

@st.cache_data(ttl=60)
def carregar_vendas_diarias():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM vendas_diarias ORDER BY data, filial", conn)
    conn.close()
    return df

df = carregar_reviews()
df_social = carregar_social()
df_news = carregar_noticias()
df_comments = carregar_pesquisa_comments()
df_perf = carregar_pesquisa_performance()
df_ifood_vendas = carregar_ifood_vendas()
df_ifood_horarios = carregar_ifood_horarios()
df_ifood_pagamentos = carregar_ifood_pagamentos()
df_ifood_dias = carregar_ifood_dias()
df_ifood_tags = carregar_ifood_tags()
df_vendas_diarias = carregar_vendas_diarias()
df_menu = carregar_menu_analysis()
df_reclamacoes = carregar_reclamacoes()
df_fila = carregar_fila_espera()
df_ifood_diario = carregar_ifood_diario()

verificar_senha()
if "aba_sel" not in st.session_state:
    st.session_state.aba_sel = "Reviews"

with st.sidebar:
    st.markdown(
        f'<div style="text-align:center; padding:10px 10px 4px;">'
        f'<img src="data:image/png;base64,{logo_b64}" width="120"/></div>'
        f'<div style="text-align:center; font-size:9px; letter-spacing:0.2em; color:#8B9A2E; text-transform:uppercase; padding-bottom:8px; margin-top:4px;">Brand Intelligence</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div style="height:1px; background:rgba(255,255,255,0.1); margin-bottom:10px;"></div>', unsafe_allow_html=True)

    aba_sel = st.session_state.aba_sel
    for aba in ["Reviews", "Social", "Pesquisa", "Analises", "Vendas", "OlivIA", "Menu", "Fila"]:
        if aba == aba_sel:
            st.markdown(f'<span class="nav-ativo">{aba}</span>', unsafe_allow_html=True)
        else:
            if st.button(aba, key=f"btn_{aba}", use_container_width=True):
                st.session_state.aba_sel = aba
                st.rerun()

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(139,154,46,0.5),transparent);margin:14px 0 10px;"></div>', unsafe_allow_html=True)

    sent_social_sel = "Todos"
    post_sel = "Todos"
    cat_sel = "Todas"
    periodo_sel = "Últimos 30 dias"
    idioma_sel = "Todos"
    plataforma_sel = "Todas"
    filial_sel = "Todas"
    sentimento_sel = "Todos"

    if aba_sel == "Reviews":
        st.markdown('<div class="sidebar-label">Filial</div>', unsafe_allow_html=True)
        filiais = ["Todas"] + sorted(df["filial"].dropna().unique().tolist())
        filial_sel = st.selectbox("Filial", filiais, key="filial", label_visibility="collapsed")
        st.markdown('<div class="sidebar-label">Plataforma</div>', unsafe_allow_html=True)
        plataformas = ["Todas"] + sorted(df["plataforma"].dropna().unique().tolist())
        plataforma_sel = st.selectbox("Plataforma", plataformas, key="plat", label_visibility="collapsed")
        st.markdown('<div class="sidebar-label">Sentimento</div>', unsafe_allow_html=True)
        sentimento_sel = st.selectbox("Sentimento", ["Todos", "Positivo", "Negativo"], key="sent", label_visibility="collapsed")

    elif aba_sel == "Social":
        st.markdown('<div class="sidebar-label">Sentimento</div>', unsafe_allow_html=True)
        sent_social_sel = st.selectbox("Sentimento", ["Todos", "Positivo", "Negativo"], key="sent_social", label_visibility="collapsed")
        st.markdown('<div class="sidebar-label">Post</div>', unsafe_allow_html=True)
        posts_unicos = ["Todos"] + [f"Post {i+1}" for i in range(df_social["post_url"].nunique())]
        post_sel = st.selectbox("Post", posts_unicos, key="post_sel", label_visibility="collapsed")

    elif aba_sel == "Notícias":
        st.markdown('<div class="sidebar-label">Categoria</div>', unsafe_allow_html=True)
        cat_sel = st.selectbox("Categoria", ["Todas", "Olive Garden Global", "Olive Garden Brasil", "Mercado A&B Brasil", "Mercado Global"], key="cat_news_side", label_visibility="collapsed")
        st.markdown('<div class="sidebar-label">Período</div>', unsafe_allow_html=True)
        periodo_sel = st.selectbox("Período", ["Últimos 30 dias", "Últimos 15 dias", "Últimos 7 dias"], key="periodo_news", label_visibility="collapsed")
        st.markdown('<div class="sidebar-label">Idioma</div>', unsafe_allow_html=True)
        idioma_sel = st.selectbox("Idioma", ["Todos", "Português", "Inglês"], key="idioma_news", label_visibility="collapsed")

    st.markdown('<div style="height:1px; background:rgba(255,255,255,0.1); margin:10px 0;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:9px; color:#8B9A2E; letter-spacing:0.1em; text-align:center;">Atualizado automaticamente<br>a cada 5 minutos</div>',
        unsafe_allow_html=True
    )

if aba_sel == "Reviews":
    st.markdown('<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Reviews & Reputacao</div>', unsafe_allow_html=True)

    df_recl = df_reclamacoes.copy()
    df_recl["data"] = pd.to_datetime(df_recl["data"])

    # Filtros
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        unidades_disp = ["Todas"] + sorted(df_recl["unidade_curta"].dropna().unique().tolist())
        unidade_recl = st.selectbox("Unidade:", unidades_disp, key="recl_unidade")
    with col_f2:
        temas_disp = ["Todos"] + sorted(df_recl["tema"].dropna().unique().tolist())
        tema_recl = st.selectbox("Tema:", temas_disp, key="recl_tema")
    with col_f3:
        canais_disp = ["Todos"] + sorted(df_recl["canal"].dropna().unique().tolist())
        canal_recl = st.selectbox("Canal:", canais_disp, key="recl_canal")

    df_rf = df_recl.copy()
    if unidade_recl != "Todas":
        df_rf = df_rf[df_rf["unidade_curta"] == unidade_recl]
    if tema_recl != "Todos":
        df_rf = df_rf[df_rf["tema"] == tema_recl]
    if canal_recl != "Todos":
        df_rf = df_rf[df_rf["canal"] == canal_recl]

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 1 — RADAR DA REDE
    with st.container(border=True):
        st.markdown('<div class="section-title">Radar da Rede</div>', unsafe_allow_html=True)
        total_recl = len(df_rf)
        data_min = df_rf["data"].min()
        data_max = df_rf["data"].max()
        meses_periodo = max(1, ((data_max - data_min).days / 30)) if pd.notna(data_min) and pd.notna(data_max) else 1
        recl_mes = total_recl / meses_periodo
        nota_media = df_rf["avaliacao"].mean() if df_rf["avaliacao"].notna().any() else 0
        pct_google = len(df_rf[df_rf["canal"]=="google_my_business"]) / total_recl * 100 if total_recl > 0 else 0
        tema_top = df_rf["tema"].value_counts().index[0] if len(df_rf) > 0 and df_rf["tema"].notna().any() else "—"
        col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns(5)
        with col_r1:
            st.metric("Reclamacoes", total_recl)
        with col_r2:
            st.metric("Recl./Mes", f"{recl_mes:.1f}")
        with col_r3:
            cor_nota = "#2e6b3e" if nota_media >= 3 else "#B8923A" if nota_media >= 2 else VERMELHO
            st.markdown(f'<div style="text-align:center;"><div style="font-size:12px;color:#8B7A5A;">Nota Media</div><div style="font-size:24px;font-weight:700;color:{cor_nota};">{nota_media:.2f}</div></div>', unsafe_allow_html=True)
        with col_r4:
            st.metric("Via Google", f"{pct_google:.0f}%")
        with col_r5:
            st.metric("Tema #1", tema_top)

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 2 — COMPARATIVO POR UNIDADE
    with st.container(border=True):
        st.markdown('<div class="section-title">Comparativo por Unidade</div>', unsafe_allow_html=True)
        unidades_ord = ["Morumbi","Center Norte","Dom Pedro","Aricanduva","Guarulhos GRU3","Guarulhos GRU2"]
        rows_tab = []
        for un in unidades_ord:
            df_un = df_recl[df_recl["unidade_curta"]==un]
            if len(df_un) == 0:
                continue
            n = len(df_un)
            d_min = df_un["data"].min()
            d_max = df_un["data"].max()
            meses_un = max(1, (d_max - d_min).days / 30)
            rpm = n / meses_un
            nota_un = df_un["avaliacao"].mean() if df_un["avaliacao"].notna().any() else 0
            tema_un = df_un["tema"].value_counts().index[0] if df_un["tema"].notna().any() else "—"
            subtema_un = df_un["subtema"].value_counts().index[0] if df_un["subtema"].notna().any() else "—"
            rows_tab.append({"Unidade": un, "Recl.": n, "Recl./Mes": f"{rpm:.1f}", "Nota": nota_un, "Tema #1": tema_un, "Dor Principal": subtema_un})
        df_tab_un = pd.DataFrame(rows_tab)
        for _, row in df_tab_un.iterrows():
            nota_v = row["Nota"]
            cor_n = "#2e6b3e" if nota_v >= 3 else "#B8923A" if nota_v >= 2 else VERMELHO
            st.markdown(
                f'<div style="display:flex;align-items:center;padding:10px 0;border-bottom:1px solid #e8ddc8;gap:12px;">' +
                f'<div style="flex:2;font-size:12px;font-weight:700;color:#3D2B1F;">{row["Unidade"]}</div>' +
                f'<div style="flex:1;text-align:center;"><div style="font-size:9px;color:#8B7A5A;">RECL.</div><div style="font-size:14px;font-weight:700;color:#3D2B1F;">{row["Recl."]}</div></div>' +
                f'<div style="flex:1;text-align:center;"><div style="font-size:9px;color:#8B7A5A;">RECL./MES</div><div style="font-size:14px;font-weight:700;color:#3D2B1F;">{row["Recl./Mes"]}</div></div>' +
                f'<div style="flex:1;text-align:center;"><div style="font-size:9px;color:#8B7A5A;">NOTA</div><div style="font-size:14px;font-weight:700;color:{cor_n};">{nota_v:.2f}</div></div>' +
                f'<div style="flex:2;text-align:center;"><div style="font-size:9px;color:#8B7A5A;">TEMA #1</div><div style="font-size:11px;color:#3D2B1F;">{row["Tema #1"]}</div></div>' +
                f'<div style="flex:3;"><div style="font-size:9px;color:#8B7A5A;">DOR PRINCIPAL</div><div style="font-size:11px;color:#3D2B1F;">{row["Dor Principal"]}</div></div></div>',
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 3 — EVOLUCAO MENSAL
    with st.container(border=True):
        st.markdown('<div class="section-title">Evolucao Mensal de Reclamacoes</div>', unsafe_allow_html=True)
        df_evo_recl = df_rf.copy()
        df_evo_recl["mes"] = df_evo_recl["data"].dt.to_period("M").astype(str)
        cores_un = {"Morumbi":"#B8923A","Center Norte":"#4A90D9","Dom Pedro":"#2e6b3e","Aricanduva":"#c0392b","Guarulhos GRU3":"#8B7A5A","Guarulhos GRU2":"#9B59B6"}
        # Total por mes (para calcular %)
        df_total_mes = df_evo_recl.groupby("mes").size().reset_index(name="total")
        fig_evo_recl = go.Figure()
        for un in unidades_ord:
            df_un_evo = df_evo_recl[df_evo_recl["unidade_curta"]==un].groupby("mes").size().reset_index(name="n")
            if len(df_un_evo) == 0:
                continue
            df_un_evo = df_un_evo.merge(df_total_mes, on="mes", how="left")
            df_un_evo["pct"] = (df_un_evo["n"] / df_un_evo["total"] * 100).round(1)
            cor = cores_un.get(un, MARROM)
            fig_evo_recl.add_trace(go.Scatter(
                x=df_un_evo["mes"], y=df_un_evo["n"],
                mode="lines+markers", name=un,
                line=dict(color=cor, width=2),
                marker=dict(size=7, color=cor),
                yaxis="y1", legendgroup=un, showlegend=True
            ))
            fig_evo_recl.add_trace(go.Scatter(
                x=df_un_evo["mes"], y=df_un_evo["pct"],
                mode="lines", name=f"{un} %",
                line=dict(color=cor, width=1.5, dash="dot"),
                yaxis="y2", legendgroup=un, showlegend=False,
                hovertemplate="%{y:.1f}%<extra>" + un + " share</extra>"
            ))
        fig_evo_recl.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10,b=10,l=10,r=60),
            xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM), showgrid=False),
            yaxis=dict(title="Reclamacoes", showgrid=True, gridcolor="#E8DCC8",
                       tickfont=dict(family="Nunito", size=10, color=MARROM)),
            yaxis2=dict(title="Share %", overlaying="y", side="right", showgrid=False,
                        tickfont=dict(family="Nunito", size=10, color=MARROM),
                        ticksuffix="%", range=[0, 60]),
            legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
            font=dict(family="Nunito"), height=320
        )
        st.markdown('<div style="font-size:10px;color:#8B7A5A;margin-bottom:4px;">Linha solida = volume ? Linha tracejada = % do total da rede</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_evo_recl, use_container_width=True, key="fig_evo_recl")

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 4 — MIX DE TEMAS
    with st.container(border=True):
        st.markdown('<div class="section-title">Mix de Temas</div>', unsafe_allow_html=True)
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Rede Geral</div>', unsafe_allow_html=True)
            temas_rede = df_rf["tema"].value_counts().reset_index()
            temas_rede.columns = ["tema","n"]
            fig_temas = go.Figure(go.Bar(
                y=temas_rede["tema"], x=temas_rede["n"],
                orientation="h",
                marker_color=[VERDE if i==0 else "#B8923A" if i==1 else "#8B7A5A" for i in range(len(temas_rede))],
                text=temas_rede["n"], textposition="outside",
                textfont=dict(family="Nunito", size=10, color=MARROM)
            ))
            fig_temas.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)),
                font=dict(family="Nunito"), height=280)
            st.plotly_chart(fig_temas, use_container_width=True, key="fig_temas_recl")
        with col_t2:
            st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Subtemas — Top 10</div>', unsafe_allow_html=True)
            subtemas_rede = df_rf["subtema"].dropna().value_counts().head(10).reset_index()
            subtemas_rede.columns = ["subtema","n"]
            fig_sub = go.Figure(go.Bar(
                y=subtemas_rede["subtema"], x=subtemas_rede["n"],
                orientation="h",
                marker_color=VERMELHO,
                text=subtemas_rede["n"], textposition="outside",
                textfont=dict(family="Nunito", size=10, color=MARROM)
            ))
            fig_sub.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)),
                font=dict(family="Nunito"), height=280)
            st.plotly_chart(fig_sub, use_container_width=True, key="fig_sub_recl")

    st.markdown("<br>", unsafe_allow_html=True)

    # BLOCO 5 — VOZ DO CLIENTE
    with st.container(border=True):
        st.markdown('<div class="section-title">Voz do Cliente</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Reclamacoes reais do Buzzmonitor (Google + Instagram) — filtradas por unidade, tema e canal acima.</div>', unsafe_allow_html=True)
        df_voz = df_rf.sort_values("data", ascending=False).head(100)
        html_voz = ""
        for _, row in df_voz.iterrows():
            nota_v = row["avaliacao"]
            cor_nota_v = "#2e6b3e" if pd.notna(nota_v) and nota_v >= 3 else "#B8923A" if pd.notna(nota_v) and nota_v >= 2 else VERMELHO
            estrelas = "★" * int(nota_v) if pd.notna(nota_v) else "—"
            canal_icon = "📱 Instagram" if row["canal"] == "instagram" else "🔍 Google"
            tema_badge = row["tema"] if pd.notna(row["tema"]) else ""
            subtema_badge = row["subtema"] if pd.notna(row["subtema"]) else ""
            html_voz += (
                f'<div style="padding:12px 0;border-bottom:1px solid #e8ddc8;">' +
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">' +
                f'<div style="display:flex;gap:8px;align-items:center;">' +
                f'<span style="font-size:10px;font-weight:700;color:#3D2B1F;">{row["unidade_curta"]}</span>' +
                f'<span style="font-size:9px;background:#e8ddc8;color:#3D2B1F;padding:2px 6px;border-radius:4px;">{tema_badge}</span>' +
                (f'<span style="font-size:9px;background:#f5e8e8;color:#8B2E2E;padding:2px 6px;border-radius:4px;">{subtema_badge}</span>' if subtema_badge else "") +
                f'</div>' +
                f'<div style="display:flex;gap:8px;align-items:center;">' +
                f'<span style="font-size:11px;color:{cor_nota_v};font-weight:700;">{estrelas}</span>' +
                f'<span style="font-size:10px;color:#8B7A5A;">{canal_icon} {str(row["data"])[:10]}</span>' +
                f'</div></div>' +
                f'<div style="font-size:12px;color:#3D2B1F;line-height:1.5;">{str(row["comentario"])[:300]}{"..." if len(str(row["comentario"])) > 300 else ""}</div></div>'
            )
        st.markdown(f'<div style="height:420px;overflow-y:auto;padding-right:8px;">{html_voz}</div>', unsafe_allow_html=True)

    # BLOCO 6 — REPUTACAO DIGITAL
    with st.container(border=True):
        st.markdown('<div class="section-title">Reputacao Digital — iFood, Google e TripAdvisor</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Reviews coletados das plataformas digitais — complemento às reclamacoes do Buzzmonitor.</div>', unsafe_allow_html=True)

        df_rev = df.copy()
        df_rev = df_rev[df_rev["sentimento"].notna()]

        # KPIs por plataforma
        col_p1, col_p2, col_p3 = st.columns(3)
        plataformas = [("iFood","#B8923A"),("Google Reviews","#4A90D9"),("TripAdvisor","#2e6b3e")]
        for col_p, (plat, cor) in zip([col_p1,col_p2,col_p3], plataformas):
            df_plat = df_rev[df_rev["plataforma"]==plat]
            n = len(df_plat)
            nota = df_plat["nota"].mean() if df_plat["nota"].notna().any() else 0
            pct_pos = len(df_plat[df_plat["sentimento"]=="Positivo"]) / n * 100 if n > 0 else 0
            with col_p:
                with st.container(border=True):
                    st.markdown(
                        f'<div style="text-align:center;padding:8px;">' +
                        f'<div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:6px;">{plat.upper()}</div>' +
                        f'<div style="font-size:28px;font-weight:800;color:{cor};">{"★"*int(round(nota))}</div>' +
                        f'<div style="font-size:20px;font-weight:700;color:{cor};">{nota:.1f}</div>' +
                        f'<div style="font-size:10px;color:#8B7A5A;">{n} reviews | {pct_pos:.0f}% positivos</div></div>',
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Distribuicao de notas
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Distribuicao de Notas por Plataforma</div>', unsafe_allow_html=True)
            fig_notas = go.Figure()
            for plat, cor in plataformas:
                df_plat = df_rev[df_rev["plataforma"]==plat]
                dist = df_plat["nota"].dropna().value_counts().sort_index()
                fig_notas.add_trace(go.Bar(
                    x=[str(int(n))+"★" for n in dist.index],
                    y=dist.values,
                    name=plat,
                    marker_color=cor
                ))
            fig_notas.update_layout(
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=10),
                xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM), showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                font=dict(family="Nunito"), height=260
            )
            st.plotly_chart(fig_notas, use_container_width=True, key="fig_notas_rev")
        with col_d2:
            st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Sentimento por Plataforma</div>', unsafe_allow_html=True)
            sent_data = []
            for plat, cor in plataformas:
                df_plat = df_rev[df_rev["plataforma"]==plat]
                for sent in ["Positivo","Neutro","Negativo"]:
                    n_sent = len(df_plat[df_plat["sentimento"]==sent])
                    sent_data.append({"plataforma":plat,"sentimento":sent,"n":n_sent})
            df_sent = pd.DataFrame(sent_data)
            cores_sent = {"Positivo":"#2e6b3e","Neutro":"#B8923A","Negativo":VERMELHO}
            fig_sent = go.Figure()
            for sent in ["Positivo","Neutro","Negativo"]:
                df_s = df_sent[df_sent["sentimento"]==sent]
                fig_sent.add_trace(go.Bar(
                    x=df_s["plataforma"], y=df_s["n"],
                    name=sent, marker_color=cores_sent[sent]
                ))
            fig_sent.update_layout(
                barmode="stack",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=10),
                xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM), showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                font=dict(family="Nunito"), height=260
            )
            st.plotly_chart(fig_sent, use_container_width=True, key="fig_sent_rev")

        st.markdown("<br>", unsafe_allow_html=True)

        # Filtros reviews
        col_rf1, col_rf2 = st.columns(2)
        with col_rf1:
            plat_sel_rev = st.selectbox("Plataforma:", ["Todas","iFood","Google Reviews","TripAdvisor"], key="rev_plat")
        with col_rf2:
            sent_sel_rev = st.selectbox("Sentimento:", ["Todos","Positivo","Neutro","Negativo"], key="rev_sent")
        fil_sel_display = st.radio("Filial:", ["Todas"] + sorted([f.replace("Olive Garden - ", "") for f in df_rev["filial"].dropna().unique().tolist() if f]), horizontal=True, key="rev_fil")
        fil_sel_rev = "Todas" if fil_sel_display == "Todas" else "Olive Garden - " + fil_sel_display

        df_rev_f = df_rev.copy()
        if plat_sel_rev != "Todas":
            df_rev_f = df_rev_f[df_rev_f["plataforma"]==plat_sel_rev]
        if sent_sel_rev != "Todos":
            df_rev_f = df_rev_f[df_rev_f["sentimento"]==sent_sel_rev]
        if fil_sel_rev != "Todas":
            df_rev_f = df_rev_f[df_rev_f["filial"]==fil_sel_rev]

        st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin:12px 0 8px 0;">Reviews Recentes</div>', unsafe_allow_html=True)
        for _, row in df_rev_f.head(30).iterrows():
            nota_r = row["nota"]
            cor_r = "#2e6b3e" if pd.notna(nota_r) and nota_r >= 4 else "#B8923A" if pd.notna(nota_r) and nota_r >= 3 else VERMELHO
            estrelas_r = "★" * int(nota_r) if pd.notna(nota_r) else "—"
            filial_r = str(row["filial"]).replace("Olive Garden - ","") if pd.notna(row["filial"]) else "—"
            texto_r = str(row.get("texto","")) if pd.notna(row.get("texto","")) else "—"
            st.markdown(
                f'<div style="padding:10px 0;border-bottom:1px solid #e8ddc8;">' +
                f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">' +
                f'<div style="display:flex;gap:8px;align-items:center;">' +
                f'<span style="font-size:10px;font-weight:700;color:#3D2B1F;">{filial_r}</span>' +
                f'<span style="font-size:9px;background:#e8ddc8;color:#3D2B1F;padding:2px 6px;border-radius:4px;">{row["plataforma"]}</span>' +
                f'</div>' +
                f'<span style="font-size:12px;color:{cor_r};font-weight:700;">{estrelas_r}</span></div>' +
                f'<div style="font-size:12px;color:#3D2B1F;line-height:1.5;">{texto_r[:250]}{"..." if len(texto_r)>250 else ""}</div></div>',
                unsafe_allow_html=True)

elif aba_sel == "Social":
    df_social_f = df_social.copy()
    if sent_social_sel != "Todos":
        df_social_f = df_social_f[df_social_f["sentimento"] == sent_social_sel]
    if post_sel != "Todos":
        post_urls = df_social["post_url"].unique()
        post_idx = int(post_sel.replace("Post ", "")) - 1
        if post_idx < len(post_urls):
            df_social_f = df_social_f[df_social_f["post_url"] == post_urls[post_idx]]

    st.markdown(
        '<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Social</div>'
        '<div style="font-size:13px; color:#8B9A2E; letter-spacing:0.1em; margin-bottom:20px;">INSTAGRAM @olivegardenbr</div>',
        unsafe_allow_html=True
    )

    total_s = len(df_social_f)
    pct_pos_s = len(df_social_f[df_social_f["sentimento"] == "Positivo"]) / total_s * 100 if total_s > 0 else 0
    pct_neg_s = len(df_social_f[df_social_f["sentimento"] == "Negativo"]) / total_s * 100 if total_s > 0 else 0
    total_likes = int(df_social_f["likes"].sum())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total de Comentários", f"{total_s:,}")
    with c2:
        st.metric("Total de Likes", f"{total_likes:,}")
    with c3:
        st.metric("Sentimento Positivo", f"{pct_pos_s:.0f}%")
    with c4:
        st.metric("Sentimento Negativo", f"{pct_neg_s:.0f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        with st.container(border=True):
            st.markdown('<div class="section-title">Polaridade dos Comentários</div>', unsafe_allow_html=True)
            contagem_s = df_social_f["sentimento"].value_counts().reset_index()
            contagem_s.columns = ["Sentimento", "Total"]
            fig_s1 = px.pie(contagem_s, values="Total", names="Sentimento", color="Sentimento", color_discrete_map=CORES_SENT, hole=0.6)
            fig_s1.update_traces(textfont_family="Nunito", textfont_size=13)
            fig_s1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), legend=dict(font=dict(family="Nunito", size=12, color=MARROM)), font=dict(family="Nunito"))
            st.plotly_chart(fig_s1, use_container_width=True, key="fig_s1")

    with col_s2:
        with st.container(border=True):
            st.markdown('<div class="section-title">Top 10 Posts por Comentários</div>', unsafe_allow_html=True)
            post_engagement = df_social.groupby("post_url").agg(
                comentarios=("texto", "count"),
                likes_total=("likes", "sum")
            ).reset_index().reset_index()
            post_engagement["label"] = post_engagement["index"].apply(lambda i: f"Post {i+1}")
            post_engagement = post_engagement.sort_values("comentarios", ascending=False).head(10)
            html_posts = ""
            for _, row in post_engagement.iterrows():
                pct = int(row["comentarios"] / post_engagement["comentarios"].max() * 100)
                html_posts += f"""<div style="margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <a href="{row['post_url']}" target="_blank" style="font-size:12px; font-weight:700; color:#5C3D1E; text-decoration:none;">{row['label']} ↗</a>
                        <span style="font-size:12px; font-weight:700; color:#3D2B1F;">{int(row['comentarios'])} comentarios</span>
                    </div>
                    <div style="background:#e8ddc8; border-radius:4px; height:8px;">
                        <div style="background:#8B9A2E; width:{pct}%; height:8px; border-radius:4px;"></div>
                    </div></div>"""
            st.markdown(html_posts, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_s3, col_s4 = st.columns(2)

    with col_s3:
        with st.container(border=True):
            st.markdown('<div class="section-title">Comentários Positivos</div>', unsafe_allow_html=True)
            pos = df_social_f[df_social_f["sentimento"] == "Positivo"].sort_values("likes", ascending=False).head(5)
            for _, row in pos.iterrows():
                st.markdown(f'<div class="comment-card"><div class="comment-autor">@{row["autor"]}</div><div class="comment-texto">{row["texto"]}</div><div class="comment-meta">❤️ {int(row["likes"])} likes</div></div>', unsafe_allow_html=True)

    with col_s4:
        with st.container(border=True):
            st.markdown('<div class="section-title">Comentários Negativos</div>', unsafe_allow_html=True)
            neg = df_social_f[df_social_f["sentimento"] == "Negativo"].sort_values("likes", ascending=False).head(5)
            for _, row in neg.iterrows():
                st.markdown(f'<div class="comment-card neg"><div class="comment-autor">@{row["autor"]}</div><div class="comment-texto">{row["texto"]}</div><div class="comment-meta">❤️ {int(row["likes"])} likes</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-title">Top Comentários por Engajamento</div>', unsafe_allow_html=True)
        top_comments = df_social_f.sort_values("likes", ascending=False).head(10).copy()
        top_comments["Post"] = top_comments["post_url"].apply(lambda url: f'<a href="{url}" target="_blank" style="color:#5C3D1E; font-weight:700;">Ver post ↗</a>')
        top_comments_display = top_comments[["autor", "texto", "sentimento", "likes", "Post"]].copy()
        top_comments_display.columns = ["Autor", "Comentário", "Sentimento", "Likes", "Post"]
        st.write(top_comments_display.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-title">Horário de Maior Engajamento</div>', unsafe_allow_html=True)
        df_social_hora = df_social_f.copy()
        df_social_hora["hora"] = pd.to_datetime(df_social_hora["data_original"], errors="coerce", utc=True).dt.hour
        df_social_hora = df_social_hora.dropna(subset=["hora"])
        if len(df_social_hora) > 0:
            hora_count = df_social_hora.groupby("hora").size().reset_index(name="comentarios")
            hora_count["hora_label"] = hora_count["hora"].apply(lambda h: f"{int(h):02d}h")
            hora_count = hora_count.sort_values("hora")
            fig_hora = px.bar(hora_count, x="hora_label", y="comentarios", color="comentarios", color_continuous_scale=[[0, BEGE], [1, VERDE]], text="comentarios")
            fig_hora.update_traces(textposition="outside", textfont=dict(family="Nunito", size=11, color=MARROM))
            fig_hora.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), coloraxis_showscale=False, xaxis=dict(title="", tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(title="", showgrid=False, tickfont=dict(family="Nunito", size=11)), font=dict(family="Nunito"))
            st.plotly_chart(fig_hora, use_container_width=True, key="fig_hora")
        else:
            st.info("Dados insuficientes para análise de horário.")

elif aba_sel == "Notícias":
    df_news_f = df_news.copy()
    if cat_sel != "Todas":
        df_news_f = df_news_f[df_news_f["categoria"] == cat_sel]
    dias = {"Últimos 30 dias": 30, "Últimos 15 dias": 15, "Últimos 7 dias": 7}
    dias_sel = dias[periodo_sel]
    data_corte = (datetime.now() - timedelta(days=dias_sel)).strftime("%Y-%m-%d")
    df_news_f = df_news_f[pd.to_datetime(df_news_f["publicado_em"], errors="coerce", utc=True) >= pd.Timestamp(data_corte, tz="UTC")]
    if idioma_sel == "Português":
        df_news_f = df_news_f[df_news_f["categoria"].str.contains("Brasil", na=False)]
    elif idioma_sel == "Inglês":
        df_news_f = df_news_f[~df_news_f["categoria"].str.contains("Brasil", na=False)]

    st.markdown(
        '<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Notícias</div>'
        '<div style="font-size:13px; color:#8B9A2E; letter-spacing:0.1em; margin-bottom:20px;">OLIVE GARDEN & MERCADO DE A&B</div>',
        unsafe_allow_html=True
    )

    total_news = len(df_news_f)
    fontes_unicas = df_news_f["fonte"].nunique()
    og_news = len(df_news_f[df_news_f["categoria"].str.contains("Olive Garden", na=False)])
    mercado_news = len(df_news_f[~df_news_f["categoria"].str.contains("Olive Garden", na=False)])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total de Notícias", f"{total_news}")
    with c2:
        st.metric("Fontes Diferentes", f"{fontes_unicas}")
    with c3:
        st.metric("Sobre Olive Garden", f"{og_news}")
    with c4:
        st.metric("Mercado A&B", f"{mercado_news}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_n1, col_n2 = st.columns(2)

    with col_n1:
        with st.container(border=True):
            st.markdown('<div class="section-title">Notícias por Categoria</div>', unsafe_allow_html=True)
            cat_count = df_news_f["categoria"].value_counts().reset_index()
            cat_count.columns = ["Categoria", "Total"]
            fig_cat = px.bar(cat_count, x="Total", y="Categoria", orientation="h", color="Total", color_continuous_scale=[[0, BEGE], [1, VERDE]], text="Total")
            fig_cat.update_traces(textposition="outside", textfont=dict(family="Nunito", size=11, color=MARROM))
            fig_cat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=40), coloraxis_showscale=False, xaxis=dict(showgrid=False, zeroline=False, title=""), yaxis=dict(title="", tickfont=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"))
            st.plotly_chart(fig_cat, use_container_width=True, key="fig_cat")

    with col_n2:
        with st.container(border=True):
            st.markdown('<div class="section-title">Principais Fontes</div>', unsafe_allow_html=True)
            fonte_count = df_news_f["fonte"].value_counts().head(10).reset_index()
            fonte_count.columns = ["Fonte", "Total"]
            fonte_count = fonte_count.sort_values("Total", ascending=True)
            fig_fonte = px.bar(fonte_count, x="Total", y="Fonte", orientation="h", color="Total", color_continuous_scale=[[0, BEGE], [1, "#4D3321"]], text="Total")
            fig_fonte.update_traces(textposition="outside", textfont=dict(family="Nunito", size=11, color=MARROM))
            fig_fonte.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=40), coloraxis_showscale=False, xaxis=dict(showgrid=False, zeroline=False, title=""), yaxis=dict(title="", tickfont=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"))
            st.plotly_chart(fig_fonte, use_container_width=True, key="fig_fonte")

    st.markdown("<br>", unsafe_allow_html=True)
    for cat in df_news_f["categoria"].unique():
        df_cat = df_news_f[df_news_f["categoria"] == cat].head(5)
        with st.container(border=True):
            st.markdown(f'<div class="section-title">{cat}</div>', unsafe_allow_html=True)
            for _, row in df_cat.iterrows():
                data = row["publicado_em"][:10] if row["publicado_em"] else ""
                st.markdown(
                    f'</div>',
                    unsafe_allow_html=True
                )

elif aba_sel == "Pesquisa":
    st.markdown(
        '<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Pesquisa Interna</div>'
        '<div style="font-size:13px; color:#8B9A2E; letter-spacing:0.1em; margin-bottom:20px;">SATISFAÇÃO DO CLIENTE — DADOS INTERNOS</div>',
        unsafe_allow_html=True
    )

    # Métricas gerais
    total_p = len(df_comments)
    pct_hs = len(df_comments[df_comments["overall_rating"] == "Highly Satisfied"]) / total_p * 100 if total_p > 0 else 0
    pct_s = len(df_comments[df_comments["overall_rating"] == "Satisfied"]) / total_p * 100 if total_p > 0 else 0
    pct_d = len(df_comments[df_comments["overall_rating"].isin(["Dissatisfied", "Highly Dissatisfied"])]) / total_p * 100 if total_p > 0 else 0
    data_min = pd.to_datetime(df_comments["survey_date"], errors="coerce").min()
    data_max = pd.to_datetime(df_comments["survey_date"], errors="coerce").max()
    df_comments_f = df_comments[df_comments["filial"].notna() & (df_comments["filial"] != "nan")].copy()
    periodo_p = f"{data_min.strftime('%d/%m/%Y')} a {data_max.strftime('%d/%m/%Y')}" if pd.notna(data_min) else "—"

    st.markdown(f'<div style="font-size:11px; color:#7a5c3a; background:#e8ddc8; padding:4px 12px; border-radius:20px; display:inline-block; margin-bottom:20px;">Período: {periodo_p}</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total de Respostas", f"{total_p:,}")
    with c2:
        st.metric("Highly Satisfied", f"{pct_hs:.0f}%")
    with c3:
        st.metric("Satisfied", f"{pct_s:.0f}%")
    with c4:
        st.metric("Insatisfeitos", f"{pct_d:.0f}%")

    st.markdown("<br>", unsafe_allow_html=True)


    # Análise cruzada 2 — Heatmap de Performance
    with st.container(border=True):
        st.markdown('<div class="section-title">Performance por Dimensão e Filial (% Topbox)</div>', unsafe_allow_html=True)
        if len(df_perf) > 0:
            df_perf_f = df_perf[df_perf["restaurant"] != "nan"].copy()
            df_perf_f["filial_curta"] = df_perf_f["restaurant"].str.replace("Olive Garden - ", "")
            df_perf_f["periodo_curto"] = df_perf_f["periodo"].str.extract(r"(FW\d+ to FW\d+)")
            df_perf_f["fw_num"] = df_perf_f["periodo_curto"].str.extract(r"FW(\d+)").astype(float)
            ultimo_periodo = df_perf_f.loc[df_perf_f["fw_num"].idxmax(), "periodo_curto"] if len(df_perf_f) > 0 else ""
            df_perf_f = df_perf_f[df_perf_f["periodo_curto"] == ultimo_periodo]
            metricas = ["overall_experience", "value", "service", "taste", "speed_of_service", "clean", "soup_salad_refill", "breadstick_refill"]
            pivot = df_perf_f.set_index("filial_curta")[metricas]
            labels = ["Experiencia Geral", "Valor", "Atendimento", "Sabor", "Velocidade", "Limpeza", "Refil Sopa/Salada", "Refil Breadstick"]
            fig_heat2 = go.Figure(data=go.Heatmap(
                z=pivot.values,
                x=labels,
                y=pivot.index.tolist(),
                colorscale=[[0, VERMELHO], [0.7, "#B8923A"], [1, VERDE]],
                zmin=70, zmax=100,
                text=pivot.values.round(1),
                texttemplate="%{text}%",
                textfont=dict(family="Nunito", size=12, color="white"),
            ))
            fig_heat2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                yaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                font=dict(family="Nunito"),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_heat2, use_container_width=True, key="fig_heat2")

    st.markdown("<br>", unsafe_allow_html=True)

    # Opcao A — Evolucao por dimensao com filtro
    with st.container(border=True):
        st.markdown('<div class="section-title">Evolucao por Dimensao e Filial</div>', unsafe_allow_html=True)
        if len(df_perf) > 1:
            df_perf_ev = df_perf[df_perf["restaurant"] != "nan"].copy()
            df_perf_ev["filial_curta"] = df_perf_ev["restaurant"].str.replace("Olive Garden - ", "")
            df_perf_ev["periodo_curto"] = df_perf_ev["periodo"].str.extract(r"(FW\d+ to FW\d+)")
            metricas_ev = {"overall_experience": "Experiencia Geral", "value": "Valor", "service": "Atendimento", "taste": "Sabor", "speed_of_service": "Velocidade", "clean": "Limpeza", "soup_salad_refill": "Refil Sopa/Salada", "breadstick_refill": "Refil Breadstick"}
            dim_sel = st.selectbox("Selecione a dimensao:", list(metricas_ev.values()), key="dim_sel")
            col_sel = [k for k, v in metricas_ev.items() if v == dim_sel][0]
            fig_ev = go.Figure()
            cores_filiais = ["#8B9A2E", "#B8923A", "#3D7A5C", "#7A3D3D", "#3D5A7A", "#7A5C3D"]
            for idx, filial in enumerate(df_perf_ev["filial_curta"].unique()):
                df_fil = df_perf_ev[df_perf_ev["filial_curta"] == filial].sort_values("periodo_curto")
                fig_ev.add_trace(go.Scatter(
                    x=df_fil["periodo_curto"],
                    y=df_fil[col_sel],
                    mode="lines+markers+text",
                    name=filial,
                    line=dict(color=cores_filiais[idx % len(cores_filiais)], width=2.5),
                    marker=dict(size=10),
                    text=df_fil[col_sel].round(1).astype(str) + "%",
                    textposition="top center",
                    textfont=dict(family="Nunito", size=11),
                ))
            fig_ev.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=20, b=10, l=10, r=10),
                legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                xaxis=dict(title="", tickfont=dict(family="Nunito", size=11, color=MARROM)),
                yaxis=dict(title="% Topbox", range=[80, 101], showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=11, color=MARROM)),
                font=dict(family="Nunito"),
                height=400,
            )
            st.plotly_chart(fig_ev, use_container_width=True, key="fig_ev")

    st.markdown("<br>", unsafe_allow_html=True)

    # Opcao C — Small multiples por filial
    with st.container(border=True):
        st.markdown('<div class="section-title">Evolucao por Filial — Todas as Dimensoes</div>', unsafe_allow_html=True)
        if len(df_perf) > 1:
            df_perf_sm = df_perf[df_perf["restaurant"] != "nan"].copy()
            df_perf_sm["filial_curta"] = df_perf_sm["restaurant"].str.replace("Olive Garden - ", "")
            df_perf_sm["periodo_curto"] = df_perf_sm["periodo"].str.extract(r"(FW\d+ to FW\d+)")
            df_perf_sm["fw_ini"] = df_perf_sm["periodo_curto"].str.extract(r"FW(\d+)").astype(float)
            metricas_sm = ["overall_experience", "value", "service", "taste", "speed_of_service", "clean", "soup_salad_refill", "breadstick_refill"]
            labels_sm = ["Exp. Geral", "Valor", "Atend.", "Sabor", "Velocidade", "Limpeza", "Refil Sopa", "Refil Bread"]
            cores_sm = ["#3D2B1F","#4A90D9","#B8923A","#2e6b3e","#c0392b","#8B7A5A","#E67E22","#9B59B6"]
            filiais_sm = sorted(df_perf_sm["filial_curta"].unique())
            # Janela deslizante — ultimas 10 semanas
            periodos_disponiveis = sorted(df_perf_sm["periodo_curto"].dropna().unique(), key=lambda p: df_perf_sm[df_perf_sm["periodo_curto"]==p]["fw_ini"].values[0] if len(df_perf_sm[df_perf_sm["periodo_curto"]==p])>0 else 0)
            ultimos_10 = periodos_disponiveis[-10:]
            df_perf_sm = df_perf_sm[df_perf_sm["periodo_curto"].isin(ultimos_10)]
            # Label curto — so FW inicial
            df_perf_sm["label_x"] = df_perf_sm["periodo_curto"].str.extract(r"^(FW\d+)")
            # Layout 3 linhas x 2 colunas
            for row_idx in range(3):
                cols_sm = st.columns(2)
                for col_idx in range(2):
                    filial_idx = row_idx * 2 + col_idx
                    if filial_idx >= len(filiais_sm):
                        break
                    filial = filiais_sm[filial_idx]
                    df_fil = df_perf_sm[df_perf_sm["filial_curta"] == filial].sort_values("fw_ini")
                    fig_sm = go.Figure()
                    for m, lbl, cor in zip(metricas_sm, labels_sm, cores_sm):
                        fig_sm.add_trace(go.Scatter(
                            x=df_fil["label_x"],
                            y=df_fil[m],
                            mode="lines+markers",
                            name=lbl,
                            line=dict(width=2, color=cor),
                            marker=dict(size=6, color=cor),
                        ))
                    fig_sm.update_layout(
                        title=dict(text=filial, font=dict(family="Nunito", size=13, color=MARROM), x=0.5),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(t=40, b=20, l=10, r=10),
                        legend=dict(font=dict(family="Nunito", size=9, color=MARROM), orientation="h", yanchor="bottom", y=-0.35, x=0),
                        xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM), showgrid=False, tickangle=-30),
                        yaxis=dict(range=[80, 101], showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=9, color=MARROM)),
                        height=320,
                        font=dict(family="Nunito"),
                    )
                    with cols_sm[col_idx]:
                        st.plotly_chart(fig_sm, use_container_width=True, key=f"fig_sm_{filial_idx}")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="section-title">Satisfação por Filial (% Highly Satisfied)</div>', unsafe_allow_html=True)
        sat_filial = df_comments_f.groupby("filial").apply(
            lambda x: len(x[x["overall_rating"] == "Highly Satisfied"]) / len(x) * 100
        ).reset_index()
        sat_filial.columns = ["filial", "pct_hs"]
        sat_filial["filial_curta"] = sat_filial["filial"].str.replace("Olive Garden - ", "")
        sat_filial = sat_filial.sort_values("pct_hs", ascending=False).reset_index(drop=True)
        cols_gauge = len(sat_filial)
        fig_sat = go.Figure()
        for idx, row in sat_filial.iterrows():
            val = row["pct_hs"]
            cor = VERDE if val >= 90 else ("#B8923A" if val >= 75 else VERMELHO)
            fig_sat.add_trace(go.Indicator(
                mode="gauge+number",
                value=val,
                title={"text": row["filial_curta"], "font": {"size": 11, "family": "Nunito", "color": MARROM}},
                number={"suffix": "%", "font": {"size": 18, "family": "Nunito", "color": cor}},
                gauge={
                    "axis": {"range": [0, 100], "tickfont": {"size": 9}},
                    "bar": {"color": cor, "thickness": 0.7},
                    "bgcolor": "#f5f0e8",
                    "steps": [
                        {"range": [0, 75], "color": "#f5e8e8"},
                        {"range": [75, 90], "color": "#f5f0df"},
                        {"range": [90, 100], "color": "#e8f2eb"},
                    ],
                },
                domain={"row": 0, "column": idx}
            ))
        fig_sat.update_layout(
            grid={"rows": 1, "columns": cols_gauge, "pattern": "independent"},
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=60, b=10, l=10, r=10),
            height=220,
            font=dict(family="Nunito")
        )
        st.plotly_chart(fig_sat, use_container_width=True, key="fig_sat")

        st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-title">Comentários Recentes da Pesquisa</div>', unsafe_allow_html=True)
        df_com_tab = df_comments[["survey_date", "filial", "overall_rating", "comentario"]].copy()
        df_com_tab["survey_date"] = pd.to_datetime(df_com_tab["survey_date"], errors="coerce").dt.strftime("%d/%m/%Y")
        df_com_tab["filial"] = df_com_tab["filial"].str.replace("Olive Garden - ", "")
        df_com_tab.columns = ["Data", "Filial", "Avaliação", "Comentário"]
        st.dataframe(df_com_tab.head(30), use_container_width=True, hide_index=True)

elif aba_sel == "Vendas":
    st.markdown('''<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Vendas</div>
    <div style="font-size:13px; color:#8B9A2E; letter-spacing:0.1em; margin-bottom:20px;">PERFORMANCE FINANCEIRA</div>''', unsafe_allow_html=True)

    visao_sel = st.radio("", ["Operacao Geral", "iFood"], horizontal=True, key="visao_vendas")
    st.markdown("<br>", unsafe_allow_html=True)

    if visao_sel == "Operacao Geral":
        import calendar
        from datetime import datetime, timedelta
        df_vd = df_vendas_diarias.copy()
        df_vd["data"] = pd.to_datetime(df_vd["data"])
        df_vd["filial_curta"] = df_vd["filial"].str.replace("Olive Garden - ", "", regex=False)

        # Filtros
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            anos = sorted(df_vd["ano"].dropna().unique().astype(int), reverse=True)
            if not list(anos):
                st.warning("Sem dados de vendas disponiveis.")
                st.stop()
            anos_sel = st.multiselect("Ano:", anos, default=[anos[0]], key="ano_vd")
            if not anos_sel:
                anos_sel = anos
        with col_f2:
            meses_ord = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]
            meses_disp = [m for m in meses_ord if m in df_vd[df_vd["ano"].isin(anos_sel)]["mes"].str[:3].str.lower().unique()]
            meses_sel = st.multiselect("Mes:", meses_disp, default=[], key="mes_vd")
            if not meses_sel:
                meses_sel = meses_disp
        with col_f3:
            filiais_disponiveis = sorted(df_vd["filial_curta"].unique())
            filiais_sel = st.multiselect("Filial:", filiais_disponiveis, default=[], key="filial_vd")
            if not filiais_sel:
                filiais_sel = filiais_disponiveis
        df_vd_f = df_vd[
            df_vd["ano"].isin(anos_sel) &
            df_vd["mes"].str[:3].str.lower().isin(meses_sel) &
            df_vd["filial_curta"].isin(filiais_sel)
        ].copy()
        vt = df_vd_f["venda_salao"].sum()
        mt = df_vd_f["meta_venda"].sum()
        va1 = df_vd_f["venda_ano1"].sum()
        gc = df_vd_f["gc_salao"].sum()
        tk = vt / gc if gc > 0 else 0
        pct_meta = 0  # calculado apos fat_if_ytd
        pct_ano1 = (vt/va1 - 1)*100 if va1 > 0 else 0
        vt_fmt = f"R$ {vt:,.0f}".replace(",",".")
        mt_fmt = f"R$ {mt:,.0f}".replace(",",".")
        va1_fmt = f"R$ {va1:,.0f}".replace(",",".")
        tk_fmt = f"R$ {tk:.0f}"
        gc_fmt = f"{int(gc):,}".replace(",",".")

        # Cards executivos
        with st.container(border=True):
            st.markdown('<div class="section-title">Visao Executiva</div>', unsafe_allow_html=True)
            # iFood MTD
            from datetime import date as _date_ve
            _hoje_ve = _date_ve.today()
            _periodo_if = f"01/{_hoje_ve.month:02d}/{_hoje_ve.year} - {_hoje_ve.day:02d}/{_hoje_ve.month:02d}/{_hoje_ve.year}"
            df_if_mtd = df_ifood_vendas[df_ifood_vendas["periodo"].str.startswith(f"01/{_hoje_ve.month:02d}/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            if len(df_if_mtd) == 0:
                df_if_mtd = df_ifood_vendas[df_ifood_vendas["periodo"].str.contains(f"/{_hoje_ve.month:02d}/{_hoje_ve.year}")] if len(df_ifood_vendas) > 0 else pd.DataFrame()
            fat_if_mtd = df_if_mtd["faturamento"].sum() if len(df_if_mtd) > 0 else 0
            # iFood filtrado — mesmo periodo do salao (anos e meses selecionados)
            if len(df_ifood_vendas) > 0:
                df_if_ytd = df_ifood_vendas[df_ifood_vendas["logistica"] == "Entrega parceira"].copy()
                # Filtrar por ano
                df_if_ytd = df_if_ytd[df_if_ytd["periodo"].str.contains("|".join([str(a) for a in anos_sel]))]
                # Filtrar por mes se nao for todos os meses
                meses_num = {"jan":"01","fev":"02","mar":"03","abr":"04","mai":"05","jun":"06","jul":"07","ago":"08","set":"09","out":"10","nov":"11","dez":"12"}
                meses_num_sel = [meses_num[m] for m in meses_sel if m in meses_num]
                if meses_num_sel and len(meses_num_sel) < 12:
                    df_if_ytd = df_if_ytd[df_if_ytd["periodo"].str[3:5].isin(meses_num_sel)]
                # Filtrar por filial
                filiais_ifood_full = ["Olive Garden - " + f for f in filiais_sel if f in ["Morumbi","Center Norte","Dom Pedro","Aricanduva"]]
                if filiais_ifood_full:
                    df_if_ytd = df_if_ytd[df_if_ytd["filial"].isin(filiais_ifood_full)]
                else:
                    df_if_ytd = pd.DataFrame()
            else:
                df_if_ytd = pd.DataFrame()
            fat_if_ytd = df_if_ytd["faturamento"].sum() if len(df_if_ytd) > 0 else 0
            # vt_total e pct_meta calculados aqui, com fat_if_ytd ja filtrado por ano/mes/filial
            vt_total = vt + fat_if_ytd
            vt_total_fmt = f"R$ {vt_total:,.0f}".replace(",",".")
            pct_meta = (vt_total/mt - 1)*100 if mt > 0 else 0
            # Calcular projecao salao para o mes atual
            import numpy as _np_proj
            import calendar as _cal_proj
            from datetime import date as _date_proj
            _hoje_proj = _date_proj.today()
            _mes_proj = _hoje_proj.month
            _ano_proj = _hoje_proj.year
            _dias_no_mes_proj = _cal_proj.monthrange(_ano_proj, _mes_proj)[1]
            df_mes_proj = df_vd[
                (df_vd["data"].dt.month == _mes_proj) &
                (df_vd["data"].dt.year == _ano_proj) &
                df_vd["filial_curta"].isin(filiais_sel)
            ].copy()
            proj_total = 0
            if len(df_mes_proj) > 0:
                _dias_real_proj = int(df_mes_proj["data"].dt.day.max())
                _venda_real_proj = df_mes_proj["venda_salao"].sum()
                df_hist_proj = df_vd[(df_vd["venda_salao"] > 0)].copy()
                df_hist_proj["dow"] = df_hist_proj["data"].dt.dayofweek
                df_hist_proj["mes_n"] = df_hist_proj["data"].dt.month
                _proj_rest = 0
                for _fil_p in filiais_sel:
                    _dff_p = df_hist_proj[df_hist_proj["filial_curta"] == _fil_p].copy()
                    if len(_dff_p) < 30:
                        continue
                    _clean_p = []
                    for _dw in _dff_p["dow"].unique():
                        _g = _dff_p[_dff_p["dow"] == _dw]
                        _q1 = _g["venda_salao"].quantile(0.10)
                        _q3 = _g["venda_salao"].quantile(0.90)
                        _iqr = _q3 - _q1
                        _clean_p.append(_g[(_g["venda_salao"] >= _q1 - 1.5*_iqr) & (_g["venda_salao"] <= _q3 + 1.5*_iqr)])
                    _dff_c = pd.concat(_clean_p)
                    _media_p = _dff_c["venda_salao"].mean()
                    _fdow_p = _dff_c.groupby("dow")["venda_salao"].mean() / _media_p
                    _fmes_p = _dff_c.groupby("mes_n")["venda_salao"].mean() / _media_p
                    _frec_p = _dff_c[_dff_c["data"] >= _dff_c["data"].max() - pd.Timedelta(days=28)]["venda_salao"].mean() / _media_p
                    _frec_p = float(_np_proj.clip(_frec_p, 0.85, 1.15))
                    for _d in range(_dias_real_proj + 1, _dias_no_mes_proj + 1):
                        _dt = pd.Timestamp(_ano_proj, _mes_proj, _d)
                        _proj_rest += _media_p * _fdow_p.get(_dt.dayofweek, 1.0) * _fmes_p.get(_mes_proj, 1.0) * _frec_p
                proj_total = _venda_real_proj + _proj_rest

            # Layout 2x3 — grid CSS
            import calendar as _cal_ve
            from datetime import date as _date_ve2
            _hoje_ve2 = _date_ve2.today()
            _dias_no_mes_ve = _cal_ve.monthrange(_hoje_ve2.year, _hoje_ve2.month)[1]
            df_mes_ve = df_vd[
                (df_vd["data"].dt.month == _hoje_ve2.month) &
                (df_vd["data"].dt.year == _hoje_ve2.year) &
                df_vd["filial_curta"].isin(filiais_sel)
            ].copy()
            _dias_realizados_ve = int(df_mes_ve["data"].dt.day.max()) if len(df_mes_ve) > 0 else 0
            _pct_conc_ve = int(_dias_realizados_ve / _dias_no_mes_ve * 100) if _dias_no_mes_ve > 0 else 0
            fat_total_mtd = vt + fat_if_ytd
            fat_total_fmt2 = f"R$ {fat_total_mtd:,.0f}".replace(",",".")
            fat_if_fmt2 = f"R$ {fat_if_ytd:,.0f}".replace(",",".")
            pct_if2 = fat_if_ytd / fat_total_mtd * 100 if fat_total_mtd > 0 else 0
            ped_if2 = int(df_if_ytd["pedidos"].sum()) if len(df_if_ytd) > 0 else 0
            tm_if2 = fat_if_ytd / ped_if2 if ped_if2 > 0 else 0
            seta_m2 = "▲" if pct_meta >= 0 else "▼"
            cor_m2 = "#4CAF7D" if pct_meta >= 0 else "#E57373"
            seta_a2 = "▲" if pct_ano1 >= 0 else "▼"
            cor_a2 = "#4CAF7D" if pct_ano1 >= 0 else "#E57373"
            hdc_ve = df_vd_f["venda_por_hdc"].mean() if len(df_vd_f) > 0 else 0
            hdc_ve_fmt = f"R$ {hdc_ve:.0f}" if pd.notna(hdc_ve) else "—"
            if len(df_mes_ve) > 0:
                proj_if_ve = (fat_if_mtd / _dias_realizados_ve * (_dias_no_mes_ve - _dias_realizados_ve)) if _dias_realizados_ve > 0 else 0
                proj_total_ve = proj_total + proj_if_ve if "proj_total" in dir() else fat_total_mtd
                # Budget fixo da tabela projecoes_gerenciais (nao oscila)
                try:
                    _conn_budg = get_conn()
                    _cur_budg = _conn_budg.cursor()
                    _cur_budg.execute("""
                        SELECT SUM(budget_mes) FROM projecoes_gerenciais
                        WHERE mes = %s AND filial = ANY(%s)
                    """, (str(_hoje_ve2.replace(day=1)),
                          ["Olive Garden - " + f for f in filiais_sel]))
                    _budg_row = _cur_budg.fetchone()
                    budget_ve = float(_budg_row[0]) if _budg_row and _budg_row[0] else 0
                    _conn_budg.close()
                except:
                    budget_ve = df_mes_ve["meta_venda"].sum() / _dias_realizados_ve * _dias_no_mes_ve if _dias_realizados_ve > 0 else 0
                pct_proj_ve = (proj_total_ve / budget_ve - 1) * 100 if budget_ve > 0 else 0
                cor_pv2 = "#4CAF7D" if pct_proj_ve >= 0 else "#E57373"
                seta_pv2 = "▲" if pct_proj_ve >= 0 else "▼"
                proj_ve_fmt = f"R$ {proj_total_ve:,.0f}".replace(",",".")
                budget_ve_fmt = f"R$ {budget_ve:,.0f}".replace(",",".")
                _proj_html = (
                    f'<div style="font-size:30px;font-weight:800;margin-bottom:8px;letter-spacing:-0.5px;">{proj_ve_fmt}</div>' +
                    f'<div style="background:rgba(255,255,255,0.15);border-radius:3px;height:3px;margin-bottom:6px;">' +
                    f'<div style="background:#8B9A2E;width:{_pct_conc_ve}%;height:3px;border-radius:3px;"></div></div>' +
                    f'<div style="font-size:10px;color:#9DC88D;margin-bottom:8px;">{_dias_realizados_ve}/{_dias_no_mes_ve} dias realizados</div>' +
                    f'<div style="display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;">' +
                    f'<span style="font-size:10px;color:#9DC88D;">Budget: {budget_ve_fmt}</span>' +
                    f'<span style="font-size:14px;font-weight:800;color:{cor_pv2};">{seta_pv2} {pct_proj_ve:+.1f}%</span></div>'
                )
            else:
                _proj_html = '<div style="font-size:12px;color:#9DC88D;margin-top:16px;">Sem dados do mes atual.</div>'

            st.markdown(f'''
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;width:100%;box-sizing:border-box;">
                <div style="background:#1a3320;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#9DC88D;letter-spacing:2px;margin-bottom:8px;">FATURAMENTO TOTAL YTD</div>
                    <div style="font-size:30px;font-weight:800;margin-bottom:8px;letter-spacing:-0.5px;">{fat_total_fmt2}</div>
                    <div style="font-size:10px;color:#9DC88D;margin-bottom:4px;">Salao: {vt_fmt} &nbsp;|&nbsp; iFood: {fat_if_fmt2}</div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:10px;color:#9DC88D;"><span>VS Budget: <b style=\"color:{cor_m2}\">{seta_m2} {pct_meta:+.1f}%</b></span><span>VS AA: <b style=\"color:{cor_a2}\">{seta_a2} {pct_ano1:+.1f}%</b></span></div><div style="border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;font-size:10px;color:#9DC88D;">{pct_if2:.1f}% do faturamento via iFood</div>
                </div>
                <div style="background:#1a3320;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#9DC88D;letter-spacing:2px;margin-bottom:8px;">PROJECAO TOTAL DO MES</div>
                    {_proj_html}
                </div>
                <div style="background:#3D2B1F;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:8px;">OPERACAO SALAO</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px;">
                        <div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">GUEST COUNT</div><div style="font-size:24px;font-weight:800;">{gc_fmt}</div></div>
                        <div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">TICKET MEDIO</div><div style="font-size:24px;font-weight:800;color:#8B9A2E;">{tk_fmt}</div></div>
                        <div><div style="font-size:9px;color:#D8CFC0;margin-bottom:2px;">VENDA / HDC</div><div style="font-size:20px;font-weight:700;color:#8B9A2E;">{hdc_ve_fmt}</div></div>
                    </div>
                </div>
            </div>
            <div style="height:12px;"></div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;width:100%;box-sizing:border-box;">
                <div style="background:#3D2B1F;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:8px;">TOTAL (SALAO+iFOOD) VS BUDGET</div>
                    <div style="font-size:28px;font-weight:800;margin-bottom:8px;">{vt_total_fmt}</div>
                    <div style="display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;">
                        <span style="font-size:10px;color:#D8CFC0;">Budget: {mt_fmt}</span>
                        <span style="font-size:16px;font-weight:800;color:{cor_m2};">{seta_m2} {pct_meta:+.1f}%</span>
                    </div>
                </div>
                <div style="background:#3D2B1F;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:8px;">VENDA SALAO VS ANO ANTERIOR</div>
                    <div style="font-size:28px;font-weight:800;margin-bottom:8px;">{vt_fmt}</div>
                    <div style="display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;">
                        <span style="font-size:10px;color:#D8CFC0;">AA: {va1_fmt}</span>
                        <span style="font-size:16px;font-weight:800;color:{cor_a2};">{seta_a2} {pct_ano1:+.1f}%</span>
                    </div>
                </div>
                <div style="background:#3D2B1F;border-radius:12px;padding:20px;color:#F5F0E8;box-sizing:border-box;">
                    <div style="font-size:9px;color:#D8CFC0;letter-spacing:2px;margin-bottom:8px;">IFOOD YTD</div>
                    <div style="font-size:28px;font-weight:800;margin-bottom:8px;">{fat_if_fmt2}</div>
                    <div style="display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.12);padding-top:8px;">
                        <span style="font-size:10px;color:#D8CFC0;">{ped_if2} pedidos</span>
                        <span style="font-size:12px;color:#8B9A2E;font-weight:700;">TM R$ {tm_if2:.0f}</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Evolucao acumulada
        with st.container(border=True):
            st.markdown('<div class="section-title">Evolucao Acumulada — Salao</div>', unsafe_allow_html=True)
            df_evo = df_vd_f.groupby("data").agg(venda_salao=("venda_salao","sum"), meta_venda=("meta_venda","sum"), venda_ano1=("venda_ano1","sum")).reset_index().sort_values("data")
            fig_evo = go.Figure()
            fig_evo.add_trace(go.Scatter(x=df_evo["data"], y=df_evo["venda_salao"].cumsum(), mode="lines", name="Realizado", line=dict(color=VERDE, width=3)))
            fig_evo.add_trace(go.Scatter(x=df_evo["data"], y=df_evo["meta_venda"].cumsum(), mode="lines", name="Budget", line=dict(color="#B8923A", width=2, dash="dot")))
            if df_evo["venda_ano1"].sum() > 0:
                fig_evo.add_trace(go.Scatter(x=df_evo["data"], y=df_evo["venda_ano1"].cumsum(), mode="lines", name="Ano Anterior", line=dict(color="#8B7A5A", width=1.5, dash="dash")))
            fig_evo.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10), xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)), yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)), legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02), font=dict(family="Nunito"), height=300)
            st.plotly_chart(fig_evo, use_container_width=True, key="fig_evo_vd")

        st.markdown("<br>", unsafe_allow_html=True)

        col_r1, col_r2 = st.columns(2)
        # Performance vs Budget por filial
        with col_r1:
            with st.container(border=True):
                st.markdown('<div class="section-title">Performance vs Budget por Filial</div>', unsafe_allow_html=True)
                # Filtra so o mes corrente para comparar com budget mensal
                from datetime import date as _date_rank
                _hoje_rank = _date_rank.today()
                _df_rank_mes = df_vd[
                    (df_vd["data"].dt.month == _hoje_rank.month) &
                    (df_vd["data"].dt.year  == _hoje_rank.year) &
                    df_vd["filial_curta"].isin(filiais_sel)
                ]
                df_rank_vd = _df_rank_mes.groupby("filial_curta").agg(venda_salao=("venda_salao","sum"), meta_venda=("meta_venda","sum")).reset_index()
                # Adiciona iFood por filial (Entrega parceira, mes corrente)
                if len(df_if_mtd) > 0:
                    _df_if_rank = df_if_mtd[df_if_mtd["logistica"]=="Entrega parceira"].copy()
                    _df_if_rank["filial_curta"] = _df_if_rank["filial"].str.replace("Olive Garden - ","",regex=False)
                    _df_if_rank = _df_if_rank[_df_if_rank["filial_curta"].isin(filiais_sel)]
                    _df_if_agg_rank = _df_if_rank.groupby("filial_curta")["faturamento"].sum().reset_index()
                    _df_if_agg_rank.columns = ["filial_curta","fat_ifood"]
                    df_rank_vd = df_rank_vd.merge(_df_if_agg_rank, on="filial_curta", how="left")
                    df_rank_vd["fat_ifood"] = df_rank_vd["fat_ifood"].fillna(0)
                else:
                    df_rank_vd["fat_ifood"] = 0
                df_rank_vd["total_mes"] = df_rank_vd["venda_salao"] + df_rank_vd["fat_ifood"]
                # Budget fixo e projecao gerencial da tabela projecoes_gerenciais
                try:
                    _conn_rank = get_conn()
                    _cur_rank = _conn_rank.cursor()
                    _cur_rank.execute("SELECT filial, budget_mes, proj_gerencial FROM projecoes_gerenciais WHERE mes = date_trunc('month', CURRENT_DATE)")
                    _budg_fil = {r[0].replace("Olive Garden - ",""): {"budget": r[1], "proj": r[2]} for r in _cur_rank.fetchall()}
                    _conn_rank.close()
                except:
                    _budg_fil = {}
                df_rank_vd["budget_fix"] = df_rank_vd["filial_curta"].map(lambda f: _budg_fil.get(f, {}).get("budget") or df_rank_vd.loc[df_rank_vd["filial_curta"]==f, "meta_venda"].values[0])
                df_rank_vd["proj_ger"]   = df_rank_vd["filial_curta"].map(lambda f: _budg_fil.get(f, {}).get("proj"))
                df_rank_vd["pct_meta"] = ((df_rank_vd["total_mes"]/df_rank_vd["budget_fix"]-1)*100).round(1)
                df_rank_vd = df_rank_vd.sort_values("pct_meta", ascending=True)
                for _, row in df_rank_vd.iterrows():
                    cor_b = "#2e6b3e" if row["pct_meta"] >= 0 else "#c0392b"
                    seta_b = "▲" if row["pct_meta"] >= 0 else "▼"
                    vd_fmt = f"R$ {row['total_mes']:,.0f}".replace(",",".")
                    proj_str = f" | Proj: R$ {row['proj_ger']:,.0f}".replace(",",".") if row["proj_ger"] else ""
                    st.markdown(f'<div style="padding:8px 0; border-bottom:1px solid #e8ddc8; display:flex; justify-content:space-between; align-items:center;"><span style="font-size:12px; font-weight:700; color:#3D2B1F;">{row["filial_curta"]}</span><div style="text-align:right;"><div style="font-size:12px; color:#3D2B1F;">{vd_fmt}{proj_str}</div><div style="font-size:12px; color:{cor_b}; font-weight:700;">{seta_b} {row["pct_meta"]:+.1f}% vs Budget</div></div></div>', unsafe_allow_html=True)

        # Sazonalidade por dia da semana
        with col_r2:
            with st.container(border=True):
                st.markdown('<div class="section-title">Ticket Medio por Unidade</div>', unsafe_allow_html=True)
                st.markdown('<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Media do periodo filtrado acima.</div>', unsafe_allow_html=True)
                df_tm = df_vd_f.groupby("filial_curta").agg(
                    venda=("venda_salao", "sum"),
                    gc=("gc_salao", "sum")
                ).reset_index()
                df_tm["ticket_medio"] = (df_tm["venda"] / df_tm["gc"]).round(2)
                df_tm = df_tm[df_tm["gc"] > 0].sort_values("ticket_medio", ascending=False)
                tm_media = df_tm["ticket_medio"].mean()
                fig_tm = go.Figure(go.Bar(
                    x=df_tm["filial_curta"],
                    y=df_tm["ticket_medio"],
                    marker_color=[VERDE if v >= tm_media else "#B8923A" for v in df_tm["ticket_medio"]],
                    text=df_tm["ticket_medio"].apply(lambda v: f"R$ {v:.2f}"),
                    textposition="outside",
                    textfont=dict(family="Nunito", size=11, color=MARROM)
                ))
                fig_tm.add_hline(y=tm_media, line_dash="dot", line_color="#B8923A",
                    annotation_text=f"Media: R$ {tm_media:.2f}",
                    annotation_font=dict(family="Nunito", size=10, color="#B8923A"))
                fig_tm.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=40),
                    xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)),
                    yaxis=dict(showgrid=False),
                    font=dict(family="Nunito"), height=280
                )
                st.plotly_chart(fig_tm, use_container_width=True, key="fig_tm_vd")

        st.markdown("<br>", unsafe_allow_html=True)

        # Comparativo mensal 2025 vs 2026
        with st.container(border=True):
            st.markdown('<div class="section-title">Comparativo Mensal 2025 vs 2026</div>', unsafe_allow_html=True)
            df_mensal = df_vd.copy()
            if filiais_sel != sorted(df_vd["filial_curta"].unique()):
                df_mensal = df_mensal[df_mensal["filial_curta"].isin(filiais_sel)]
            df_mensal["mes_num"] = pd.to_datetime(df_mensal["data"]).dt.month
            df_mensal["mes_label"] = pd.to_datetime(df_mensal["data"]).dt.strftime("%b")
            # 2025: salao puro (sem dado de iFood 2025 no banco)
            df_2025 = df_mensal[df_mensal["ano"]==2025].groupby(["mes_num","mes_label"])["venda_salao"].sum().reset_index().sort_values("mes_num")
            df_2025["total"] = df_2025["venda_salao"]
            # 2026: salao + iFood (Entrega parceira, 4 filiais)
            df_2026 = df_mensal[df_mensal["ano"]==2026].groupby(["mes_num","mes_label"])["venda_salao"].sum().reset_index().sort_values("mes_num")
            _filiais_if_sel = ["Olive Garden - " + f for f in filiais_sel]
            _df_if_mens = df_ifood_vendas[
                (df_ifood_vendas["logistica"]=="Entrega parceira") &
                (df_ifood_vendas["filial"].isin(_filiais_if_sel))
            ].copy()
            _df_if_mens["mes_num"] = _df_if_mens["periodo"].apply(lambda p: int(p.split("/")[1]))
            _df_if_mens["ano_if"] = _df_if_mens["periodo"].apply(lambda p: int(p.split("/")[2].split(" ")[0]))
            _df_if_agg = _df_if_mens[_df_if_mens["ano_if"]==2026].groupby("mes_num")["faturamento"].sum().reset_index()
            _df_if_agg.columns = ["mes_num","fat_ifood"]
            df_2026 = df_2026.merge(_df_if_agg, on="mes_num", how="left")
            df_2026["fat_ifood"] = df_2026["fat_ifood"].fillna(0)
            df_2026["total"] = df_2026["venda_salao"] + df_2026["fat_ifood"]
            df_budget = df_mensal[df_mensal["ano"]==2026].groupby(["mes_num","mes_label"])["meta_venda"].sum().reset_index().sort_values("mes_num")
            # Budget: usa projecoes_gerenciais para meses com entrada, meta_venda para os demais
            try:
                _conn_budg4 = get_conn()
                _cur_budg4 = _conn_budg4.cursor()
                _cur_budg4.execute("SELECT mes, SUM(budget_mes) FROM projecoes_gerenciais GROUP BY mes")
                _budg_mes = {r[0].month: r[1] for r in _cur_budg4.fetchall()}
                _conn_budg4.close()
                df_budget["budget_fix"] = df_budget["mes_num"].map(lambda m: _budg_mes.get(int(m)))
                df_budget["meta_final"] = df_budget.apply(
                    lambda r: r["budget_fix"] if pd.notna(r["budget_fix"]) and r["budget_fix"] > 0 else r["meta_venda"], axis=1)
                # Para meses futuros sem meta_venda no banco, usa budget da tabela
                import calendar as _cal_budg
                from datetime import date as _dt_budg
                _ano_sel = max(anos_sel) if anos_sel else _dt_budg.today().year
                _hoje_mes = _dt_budg.today().month
                for _mi, _ml in zip(df_budget["mes_num"], df_budget["mes_label"]):
                    if int(_mi) > _hoje_mes and int(_mi) in _budg_mes:
                        df_budget.loc[df_budget["mes_num"]==_mi, "meta_final"] = _budg_mes[int(_mi)]
            except:
                df_budget["meta_final"] = df_budget["meta_venda"]
            fig_mens = go.Figure()
            fig_mens.add_trace(go.Bar(x=df_2025["mes_label"], y=df_2025["total"], name="2025 (Salao)", marker_color="#8B7A5A", opacity=0.7))
            fig_mens.add_trace(go.Bar(x=df_2026["mes_label"], y=df_2026["total"], name="2026 (Salao+iFood)", marker_color=VERDE))
            fig_mens.add_trace(go.Scatter(x=df_budget["mes_label"], y=df_budget["meta_final"], name="Budget", mode="lines+markers", line=dict(color="#B8923A", width=2, dash="dot"), marker=dict(size=8, color="#B8923A", symbol="diamond")))
            fig_mens.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10), xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)), legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02), font=dict(family="Nunito"), height=300)
            st.plotly_chart(fig_mens, use_container_width=True, key="fig_mens_vd")

        st.markdown("<br>", unsafe_allow_html=True)

        # HDC por filial
        with st.container(border=True):
            st.markdown('<div class="section-title">Produtividade — Venda por HDC e por Assento</div>', unsafe_allow_html=True)
            ASSENTOS = {"Aricanduva": 174, "Center Norte": 173, "Dom Pedro": 241, "Guarulhos GRU2": 212, "Guarulhos GRU3": 124, "Morumbi": 300}
            from datetime import date as _date
            _hoje = df_vd["data"].max()
            if len(df_vd_f) > 0:
                df_mes_hdc = df_vd_f.copy()
            else:
                df_mes_hdc = df_vd[
                    (df_vd["data"].dt.month == _hoje.month) &
                    (df_vd["data"].dt.year == _hoje.year) &
                    df_vd["filial_curta"].isin(filiais_sel)
                ].copy()
            df_hdc = df_mes_hdc.groupby("filial_curta").agg(venda_salao=("venda_salao","sum"), hdc=("hdc","mean")).reset_index()
            df_hdc["venda_por_hdc"] = (df_hdc["venda_salao"] / df_hdc["hdc"]).round(0)
            df_hdc["nr_assentos"] = df_hdc["filial_curta"].map(ASSENTOS)
            df_hdc["venda_por_assento"] = (df_hdc["venda_salao"] / df_hdc["nr_assentos"]).round(0)
            df_hdc = df_hdc.sort_values("venda_por_hdc", ascending=False)
            col_hdc1, col_hdc2 = st.columns(2)
            with col_hdc1:
                st.markdown('<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Receita por Funcionario (HDC)</div>', unsafe_allow_html=True)
                media_hdc = df_hdc["venda_por_hdc"].mean()
                fig_hdc = go.Figure(go.Bar(x=df_hdc["filial_curta"], y=df_hdc["venda_por_hdc"], marker_color=[VERDE if v >= media_hdc else "#B8923A" for v in df_hdc["venda_por_hdc"]], text=df_hdc["venda_por_hdc"].apply(lambda v: f"R$ {v:.0f}"), textposition="outside", textfont=dict(family="Nunito", size=11, color=MARROM)))
                fig_hdc.add_hline(y=media_hdc, line_dash="dot", line_color="#B8923A", annotation_text=f"Media: R$ {media_hdc:.0f}", annotation_font=dict(family="Nunito", size=10, color="#B8923A"))
                fig_hdc.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=40), xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)), yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_hdc, use_container_width=True, key="fig_hdc_vd")
            with col_hdc2:
                st.markdown('<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-bottom:8px;">Receita por Assento</div>', unsafe_allow_html=True)
                df_hdc2 = df_hdc.sort_values("venda_por_assento", ascending=False)
                media_ass = df_hdc2["venda_por_assento"].mean()
                fig_ass = go.Figure(go.Bar(x=df_hdc2["filial_curta"], y=df_hdc2["venda_por_assento"], marker_color=[VERDE if v >= media_ass else "#B8923A" for v in df_hdc2["venda_por_assento"]], text=df_hdc2["venda_por_assento"].apply(lambda v: f"R$ {v:.0f}"), textposition="outside", textfont=dict(family="Nunito", size=11, color=MARROM)))
                fig_ass.add_hline(y=media_ass, line_dash="dot", line_color="#B8923A", annotation_text=f"Media: R$ {media_ass:.0f}", annotation_font=dict(family="Nunito", size=10, color="#B8923A"))
                fig_ass.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=40), xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)), yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_ass, use_container_width=True, key="fig_ass_vd")
    elif visao_sel == "iFood":
        import calendar
        from datetime import datetime
        df_v = df_ifood_vendas[df_ifood_vendas["logistica"] == "Entrega parceira"].copy()
        df_v["filial_curta"] = df_v["filial"].str.replace("Olive Garden - ", "", regex=False)
        periodos = sorted(df_v["periodo"].unique())

        # Cards executivos iFood
        with st.container(border=True):
            st.markdown('<div class="section-title">Visao Executiva</div>', unsafe_allow_html=True)
            # Calcular dados por periodo
            dados_periodos = []
            for periodo in periodos:
                df_per = df_v[df_v["periodo"] == periodo]
                fat = df_per["faturamento"].sum()
                ped = int(df_per["pedidos"].sum())
                tkt = fat / ped if ped > 0 else 0
                nov = int(df_per["novos_clientes"].sum())
                try:
                    partes = periodo.split("-")
                    d_ini = datetime.strptime(partes[0].strip(), "%d/%m/%Y")
                    d_fim = datetime.strptime(partes[1].strip(), "%d/%m/%Y")
                    dias_dec = (d_fim - d_ini).days + 1
                    dias_mes = calendar.monthrange(d_ini.year, d_ini.month)[1]
                except:
                    dias_dec = 30
                    dias_mes = 30
                dados_periodos.append({"periodo": periodo, "fat": fat, "ped": ped, "tkt": tkt, "nov": nov, "dias_dec": dias_dec, "dias_mes": dias_mes})
            # Card acumulado e mes atual
            fat_acum = df_v["faturamento"].sum()
            ped_acum = int(df_v["pedidos"].sum())
            tkt_acum = fat_acum / ped_acum if ped_acum > 0 else 0
            nov_acum = int(df_v["novos_clientes"].sum())
            mes_map = {"01":"Jan","02":"Fev","03":"Mar","04":"Abr","05":"Mai","06":"Jun","07":"Jul","08":"Ago","09":"Set","10":"Out","11":"Nov","12":"Dez"}
            fat_acum_fmt = "R$ {:,.0f}".format(fat_acum).replace(",",".")
            tkt_acum_fmt = "R$ {:.0f}".format(tkt_acum)
            dp = dados_periodos[-1]
            mes_num = dp["periodo"].split("/")[1].strip()[:2] if "/" in dp["periodo"] else ""
            mes_label = mes_map.get(mes_num, dp["periodo"][:3])
            fat_fmt = "R$ {:,.0f}".format(dp["fat"]).replace(",",".")
            tkt_fmt = "R$ {:.0f}".format(dp["tkt"])
            proj_html = ""
            if dp["dias_dec"] < dp["dias_mes"]:
                fat_proj = dp["fat"] / dp["dias_dec"] * dp["dias_mes"]
                ped_proj = int(dp["ped"] / dp["dias_dec"] * dp["dias_mes"])
                fat_proj_fmt = "R$ {:,.0f}".format(fat_proj).replace(",",".")
                proj_html = (
                    '<div style="margin-top:12px; padding-top:10px; border-top:1px solid rgba(255,255,255,0.1);">'
                    + '<div style="font-size:9px; color:#B8923A; letter-spacing:2px; margin-bottom:6px;">PROJECAO MES COMPLETO (' + str(dp["dias_mes"]) + ' dias)</div>'
                    + '<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:2px;">FATURAMENTO</div>'
                    + '<div style="font-size:14px; font-weight:700; color:#B8923A;">' + fat_proj_fmt + '</div></div>'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:2px;">PEDIDOS</div>'
                    + '<div style="font-size:14px; font-weight:700; color:#B8923A;">' + str(ped_proj) + '</div></div>'
                    + '</div>'
                    + '<div style="font-size:9px; color:#8B7A5A; margin-top:4px;">Parcial: ' + str(dp["dias_dec"]) + ' de ' + str(dp["dias_mes"]) + ' dias</div></div>'
                )
            cols_v = st.columns(2)
            with cols_v[0]:
                st.markdown(
                    '<div style="background:#1a1209; border-radius:12px; padding:20px; color:#F5F0E8; margin-bottom:8px; border:1px solid #8B9A2E;">'
                    + '<div style="font-size:10px; letter-spacing:3px; color:#8B9A2E; text-transform:uppercase; margin-bottom:14px;">ACUMULADO</div>'
                    + '<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">FATURAMENTO</div>'
                    + '<div style="font-size:22px; font-weight:800;">' + fat_acum_fmt + '</div></div>'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">PEDIDOS</div>'
                    + '<div style="font-size:22px; font-weight:800;">' + str(ped_acum) + '</div></div>'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">TICKET MEDIO</div>'
                    + '<div style="font-size:18px; font-weight:700; color:#8B9A2E;">' + tkt_acum_fmt + '</div></div>'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">NOVOS CLIENTES</div>'
                    + '<div style="font-size:18px; font-weight:700; color:#8B9A2E;">' + str(nov_acum) + '</div></div>'
                    + '</div></div>',
                    unsafe_allow_html=True
                )
            with cols_v[1]:
                st.markdown(
                    '<div style="background:#3D2B1F; border-radius:12px; padding:20px; color:#F5F0E8; margin-bottom:8px;">'
                    + '<div style="font-size:10px; letter-spacing:3px; color:#8B9A2E; text-transform:uppercase; margin-bottom:14px;">' + mes_label + ' (parcial)</div>'
                    + '<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">FATURAMENTO</div>'
                    + '<div style="font-size:22px; font-weight:800;">' + fat_fmt + '</div></div>'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">PEDIDOS</div>'
                    + '<div style="font-size:22px; font-weight:800;">' + str(dp["ped"]) + '</div></div>'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">TICKET MEDIO</div>'
                    + '<div style="font-size:18px; font-weight:700; color:#8B9A2E;">' + tkt_fmt + '</div></div>'
                    + '<div><div style="font-size:9px; color:#D8CFC0; margin-bottom:4px;">NOVOS CLIENTES</div>'
                    + '<div style="font-size:18px; font-weight:700; color:#8B9A2E;">' + str(dp["nov"]) + '</div></div>'
                    + '</div>' + proj_html + '</div>',
                    unsafe_allow_html=True
                )
        st.markdown("<br>", unsafe_allow_html=True)
        periodo_sel_v = st.selectbox("Periodo:", periodos, index=len(periodos)-1, key="periodo_v")
        df_vp = df_v[df_v["periodo"] == periodo_sel_v]

        # Ranking por filial com projecao
        with st.container(border=True):
            st.markdown('<div class="section-title">Faturamento por Filial</div>', unsafe_allow_html=True)
            df_rank = df_vp.groupby("filial_curta").agg(faturamento=("faturamento","sum"), pedidos=("pedidos","sum"), novos_clientes=("novos_clientes","sum")).reset_index()
            df_rank["ticket_medio"] = (df_rank["faturamento"] / df_rank["pedidos"]).round(0)
            df_rank = df_rank.sort_values("faturamento", ascending=True)
            df_rank["fat_fmt"] = df_rank["faturamento"].apply(lambda v: f"R$ {v:,.0f}".replace(",","."))
            is_parcial = False
            dias_decorridos = 30
            dias_no_mes = 30
            try:
                partes = periodo_sel_v.split("-")
                d_ini = datetime.strptime(partes[0].strip(), "%d/%m/%Y")
                d_fim = datetime.strptime(partes[1].strip(), "%d/%m/%Y")
                dias_decorridos = (d_fim - d_ini).days + 1
                dias_no_mes = calendar.monthrange(d_ini.year, d_ini.month)[1]
                if dias_decorridos < dias_no_mes:
                    is_parcial = True
                    df_rank["faturamento_projetado"] = (df_rank["faturamento"] / dias_decorridos * dias_no_mes).round(0)
                    df_rank["proj_fmt"] = df_rank["faturamento_projetado"].apply(lambda v: f"R$ {v:,.0f}".replace(",","."))
            except:
                pass
            fig_rank = go.Figure()
            if is_parcial:
                fig_rank.add_trace(go.Bar(y=df_rank["filial_curta"], x=df_rank["faturamento_projetado"], orientation="h", name=f"Projetado ({dias_no_mes} dias)", marker_color="#B8923A", opacity=0.4, text=df_rank["proj_fmt"], textposition="inside", textfont=dict(family="Nunito", size=12, color="white")))
            fig_rank.add_trace(go.Bar(y=df_rank["filial_curta"], x=df_rank["faturamento"], orientation="h", name=f"Realizado ({dias_decorridos} dias)" if is_parcial else "Faturamento", marker_color=VERDE, text=df_rank["fat_fmt"], textposition="inside", textfont=dict(family="Nunito", size=12, color="white")))
            if is_parcial:
                fig_rank.add_annotation(text=f"Parcial: {dias_decorridos} de {dias_no_mes} dias | Projecao linear", xref="paper", yref="paper", x=0.5, y=-0.08, showarrow=False, font=dict(family="Nunito", size=11, color="#B8923A"))
            fig_rank.update_layout(barmode="overlay", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=30,l=10,r=200), xaxis=dict(showgrid=False, tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(tickfont=dict(family="Nunito", size=12, color=MARROM)), legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.04), font=dict(family="Nunito"), height=320)
            st.plotly_chart(fig_rank, use_container_width=True, key="fig_rank_v")

        st.markdown("<br>", unsafe_allow_html=True)

        # Evolucao de receita iFood
        with st.container(border=True):
            st.markdown('<div class="section-title">Evolucao de Receita iFood</div>', unsafe_allow_html=True)
            evolucao = []
            for p in periodos:
                df_p = df_v[df_v["periodo"] == p]
                fat_p = df_p["faturamento"].sum()
                try:
                    partes = p.split("-")
                    d_ini = datetime.strptime(partes[0].strip(), "%d/%m/%Y")
                    d_fim = datetime.strptime(partes[1].strip(), "%d/%m/%Y")
                    dias_dec = (d_fim - d_ini).days + 1
                    dias_mes = calendar.monthrange(d_ini.year, d_ini.month)[1]
                    mes_map2 = {"01":"Jan","02":"Fev","03":"Mar","04":"Abr","05":"Mai","06":"Jun","07":"Jul","08":"Ago","09":"Set","10":"Out","11":"Nov","12":"Dez"}
                    mes_label2 = mes_map2.get(f"{d_ini.month:02d}", p)
                    is_p = dias_dec < dias_mes
                    fat_proj2 = fat_p / dias_dec * dias_mes if is_p else None
                    evolucao.append({"mes": mes_label2, "fat": fat_p, "proj": fat_proj2, "parcial": is_p})
                except:
                    evolucao.append({"mes": p[:3], "fat": fat_p, "proj": None, "parcial": False})
            fig_evo2 = go.Figure()
            meses2 = [e["mes"] for e in evolucao]
            fats2 = [e["fat"] for e in evolucao]
            fig_evo2.add_trace(go.Scatter(x=meses2, y=fats2, mode="lines+markers+text", name="Realizado", line=dict(color=VERDE, width=3), marker=dict(size=10, color=VERDE), text=[f"R$ {v:,.0f}".replace(",",".") for v in fats2], textposition="top center", textfont=dict(family="Nunito", size=11, color=VERDE)))
            for i_e, e in enumerate(evolucao):
                if e["parcial"] and e["proj"]:
                    fig_evo2.add_trace(go.Scatter(x=[meses2[i_e], meses2[i_e]], y=[fats2[i_e], e["proj"]], mode="lines+markers+text", name="Projetado", line=dict(color="#B8923A", width=2, dash="dot"), marker=dict(size=10, color="#B8923A", symbol="diamond"), text=["", f"R$ {e['proj']:,.0f}".replace(",",".")], textposition="top center", textfont=dict(family="Nunito", size=11, color="#B8923A"), showlegend=True))
            fig_evo2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=30,b=10,l=10,r=10), xaxis=dict(tickfont=dict(family="Nunito", size=12, color=MARROM), showgrid=False), yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=11, color=MARROM)), legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02), font=dict(family="Nunito"), height=350)
            st.plotly_chart(fig_evo2, use_container_width=True, key="fig_evo_v2")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="section-title">Evolucao de Receita iFood por Unidade</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Faturamento mensal iFood (Entrega parceira) por filial. Mes parcial projetado para o mes cheio (linha tracejada).</div>', unsafe_allow_html=True)
            _cores_fil = {
                "Olive Garden - Morumbi":       "#2a78d6",
                "Olive Garden - Center Norte":  "#1baf7a",
                "Olive Garden - Dom Pedro":     "#B8923A",
                "Olive Garden - Aricanduva":    "#e34948",
            }
            _filiais_if = ["Olive Garden - Morumbi","Olive Garden - Center Norte","Olive Garden - Dom Pedro","Olive Garden - Aricanduva"]
            _mes_map3 = {"01":"Jan","02":"Fev","03":"Mar","04":"Abr","05":"Mai","06":"Jun","07":"Jul","08":"Ago","09":"Set","10":"Out","11":"Nov","12":"Dez"}
            _evo_fil = {f: [] for f in _filiais_if}
            _meses3 = []
            for _p3 in periodos:
                try:
                    _pt3 = _p3.split("-")
                    _di3 = datetime.strptime(_pt3[0].strip(), "%d/%m/%Y")
                    _df3 = datetime.strptime(_pt3[1].strip(), "%d/%m/%Y")
                    _dd3 = (_df3 - _di3).days + 1
                    _dm3 = calendar.monthrange(_di3.year, _di3.month)[1]
                    _ml3 = _mes_map3.get(f"{_di3.month:02d}", _p3)
                    _isp3 = _dd3 < _dm3
                except:
                    _ml3 = _p3[:3]; _isp3 = False; _dd3 = 30; _dm3 = 30
                _meses3.append(_ml3)
                for _f3 in _filiais_if:
                    _fat3 = df_v[(df_v["periodo"]==_p3)&(df_v["filial"]==_f3)]["faturamento"].sum()
                    _fat_adj3 = _fat3/_dd3*_dm3 if _isp3 and _fat3>0 else _fat3
                    _evo_fil[_f3].append({"fat": _fat3, "fat_adj": _fat_adj3, "parcial": _isp3})
            fig_evo_fil = go.Figure()
            for _f3 in _filiais_if:
                _nome3 = _f3.replace("Olive Garden - ","")
                _cor3 = _cores_fil[_f3]
                _vals_r = [e["fat"] for e in _evo_fil[_f3]]
                _vals_a = [e["fat_adj"] for e in _evo_fil[_f3]]
                _isp_list = [e["parcial"] for e in _evo_fil[_f3]]
                _x_real = [_meses3[i] for i in range(len(_meses3)) if not _isp_list[i]]
                _y_real = [_vals_r[i] for i in range(len(_meses3)) if not _isp_list[i]]
                if _x_real:
                    fig_evo_fil.add_trace(go.Scatter(
                        x=_x_real, y=_y_real, mode="lines+markers", name=_nome3,
                        line=dict(color=_cor3, width=2), marker=dict(size=7, color=_cor3),
                        legendgroup=_nome3, showlegend=True))
                for i in range(len(_meses3)):
                    if _isp_list[i] and _vals_r[i] > 0:
                        _x_ant = _meses3[i-1] if i > 0 else None
                        _y_ant = _vals_r[i-1] if i > 0 else None
                        if _x_ant:
                            fig_evo_fil.add_trace(go.Scatter(
                                x=[_x_ant, _meses3[i]], y=[_y_ant, _vals_a[i]],
                                mode="lines+markers+text", name=_nome3+" (proj)",
                                line=dict(color=_cor3, width=2, dash="dot"),
                                marker=dict(size=7, color=_cor3, symbol="diamond"),
                                text=["", f"R$ {_vals_a[i]:,.0f}".replace(",",".")],
                                textposition="top center",
                                textfont=dict(family="Nunito", size=10, color=_cor3),
                                legendgroup=_nome3, showlegend=False))
            fig_evo_fil.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=30,b=10,l=10,r=10), height=360,
                xaxis=dict(tickfont=dict(family="Nunito", size=12, color=MARROM), showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=11, color=MARROM),
                           tickformat=",.0f", tickprefix="R$ "),
                legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                font=dict(family="Nunito"))
            st.plotly_chart(fig_evo_fil, use_container_width=True, key="fig_evo_fil_ifood")

        with st.container(border=True):
            st.markdown('<div class="section-title">Vendas Diarias — Mes Corrente</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Faturamento iFood por dia do mes corrente. Atualizado diariamente.</div>', unsafe_allow_html=True)
            if len(df_ifood_diario) > 0:
                df_id = df_ifood_diario.copy()
                df_id["data"] = pd.to_datetime(df_id["data"])
                _hoje_id = df_id["data"].max()
                df_id_mes = df_id[(df_id["data"].dt.month == _hoje_id.month) & (df_id["data"].dt.year == _hoje_id.year)]
                df_id_rede = df_id_mes.groupby("data").agg(faturamento=("faturamento","sum"), pedidos=("pedidos","sum")).reset_index().sort_values("data")
                fig_diario = go.Figure()
                fig_diario.add_trace(go.Bar(
                    x=df_id_rede["data"].dt.strftime("%d/%m"),
                    y=df_id_rede["faturamento"],
                    marker_color=VERDE,
                    text=df_id_rede["faturamento"].apply(lambda v: f"R$ {v:,.0f}".replace(",",".")),
                    textposition="outside",
                    textfont=dict(family="Nunito", size=9, color=MARROM)
                ))
                fat_acum = df_id_rede["faturamento"].sum()
                fig_diario.add_hline(
                    y=df_id_rede["faturamento"].mean(),
                    line_dash="dot", line_color="#B8923A",
                    annotation_text=f"Media: R$ {df_id_rede['faturamento'].mean():,.0f}".replace(',','.'),
                    annotation_font=dict(size=10, color="#B8923A")
                )
                fig_diario.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM), showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM), tickprefix="R$ "),
                    font=dict(family="Nunito"), height=300
                )
                st.plotly_chart(fig_diario, use_container_width=True, key="fig_diario_ifood")
                col_d1, col_d2, col_d3 = st.columns(3)
                with col_d1: st.metric("MTD Diario", f"R$ {fat_acum:,.0f}".replace(",","."))
                with col_d2: st.metric("Dias com dados", len(df_id_rede))
                with col_d3: st.metric("Media/dia", f"R$ {df_id_rede['faturamento'].mean():,.0f}".replace(",","."))
            else:
                st.info("Sem dados diarios. Rode importar_ifood_diario.py apos subir o arquivo em data/ifood_diario/.")

        st.markdown("<br>", unsafe_allow_html=True)


        with st.container(border=True):
            st.markdown('<div class="section-title">Share iFood na Receita Total (Salao + iFood)</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">% do faturamento total representado pelo iFood a cada mes.</div>', unsafe_allow_html=True)
            share_data = []
            df_vd_share = df_vendas_diarias.copy()
            df_vd_share["data"] = pd.to_datetime(df_vd_share["data"])
            df_vd_share["mes_ano"] = df_vd_share["data"].dt.strftime("%m/%Y")
            venda_salao_mes = df_vd_share.groupby("mes_ano")["venda_salao"].sum().reset_index()
            venda_salao_mes.columns = ["mes_ano", "salao"]
            mes_map_share = {"01":"Jan","02":"Fev","03":"Mar","04":"Abr","05":"Mai","06":"Jun","07":"Jul","08":"Ago","09":"Set","10":"Out","11":"Nov","12":"Dez"}
            for p in periodos:
                try:
                    partes = p.split("-")
                    d_ini = datetime.strptime(partes[0].strip(), "%d/%m/%Y")
                    mes_ano_key = f"{d_ini.month:02d}/{d_ini.year}"
                    fat_if_p = df_v[df_v["periodo"] == p]["faturamento"].sum()
                    # Apenas filiais com iFood
                    filiais_com_ifood = ["Olive Garden - Morumbi","Olive Garden - Center Norte","Olive Garden - Aricanduva","Olive Garden - Dom Pedro"]
                    venda_salao_ifood = df_vd_share[df_vd_share["filial"].isin(filiais_com_ifood)].groupby("mes_ano")["venda_salao"].sum().reset_index()
                    venda_salao_ifood.columns = ["mes_ano","salao"]
                    salao_p = venda_salao_ifood[venda_salao_ifood["mes_ano"] == mes_ano_key]["salao"].sum()
                    total_p = salao_p + fat_if_p
                    share_p = fat_if_p / total_p * 100 if total_p > 0 else 0
                    mes_label_s = mes_map_share.get(f"{d_ini.month:02d}", p[:3])
                    share_data.append({"mes": mes_label_s, "share": share_p, "fat_if": fat_if_p, "salao": salao_p, "total": total_p})
                except:
                    pass
            if len(share_data) > 0:
                fig_share = go.Figure()
                cores_filial = {
                    "Morumbi": "#B8923A",
                    "Center Norte": "#4A90D9",
                    "Aricanduva": "#2e6b3e",
                    "Dom Pedro": "#c0392b",
                }
                filiais_ifood = [f for f in ["Morumbi","Center Norte","Aricanduva","Dom Pedro"]]
                # Linha por unidade
                for filial_if in filiais_ifood:
                    filial_full = "Olive Garden - " + filial_if
                    share_fil = []
                    for p in periodos:
                        try:
                            partes = p.split("-")
                            d_ini = datetime.strptime(partes[0].strip(), "%d/%m/%Y")
                            mes_ano_key = f"{d_ini.month:02d}/{d_ini.year}"
                            fat_if_fil = df_v[(df_v["periodo"]==p) & (df_v["filial"]==filial_full)]["faturamento"].sum() if "filial" in df_v.columns else 0
                            salao_fil_v = df_vd_share[(df_vd_share["mes_ano"]==mes_ano_key) & (df_vd_share["filial"].str.contains(filial_if, na=False))]["venda_salao"].sum()
                            total_fil = salao_fil_v + fat_if_fil
                            share_fil.append(fat_if_fil/total_fil*100 if total_fil>0 else 0)
                        except:
                            share_fil.append(0)
                    meses_s = [s["mes"] for s in share_data]
                    fig_share.add_trace(go.Scatter(
                        x=meses_s, y=share_fil,
                        mode="lines+markers",
                        name=filial_if,
                        line=dict(color=cores_filial.get(filial_if, MARROM), width=2, dash="dot"),
                        marker=dict(size=7, color=cores_filial.get(filial_if, MARROM)),
                        hovertemplate=f"<b>{filial_if}</b><br>%{{x}}: %{{y:.1f}}<extra></extra>"
                    ))
                # Linha rede geral
                meses_s = [s["mes"] for s in share_data]
                shares_s = [s["share"] for s in share_data]
                fig_share.add_trace(go.Scatter(
                    x=meses_s, y=shares_s,
                    mode="lines+markers+text",
                    name="Rede Geral",
                    line=dict(color=VERDE, width=3),
                    marker=dict(size=10, color=VERDE),
                    text=[f"{v:.1f}%" for v in shares_s],
                    textposition="top center",
                    textfont=dict(family="Nunito", size=10, color=VERDE),
                    hovertemplate="<b>Rede</b><br>%{x}: %{y:.1f}%<extra></extra>"
                ))
                fig_share.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=30,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=12, color=MARROM), showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=11, color=MARROM), ticksuffix="%"),
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                    font=dict(family="Nunito"), height=340
                )
                st.plotly_chart(fig_share, use_container_width=True, key="fig_share_ifood")

        st.markdown("<br>", unsafe_allow_html=True)
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            with st.container(border=True):
                st.markdown('<div class="section-title">Horario de Pico</div>', unsafe_allow_html=True)
                df_hor = df_ifood_horarios[df_ifood_horarios["periodo"] == periodo_sel_v].groupby(["periodo_semana","horario"])["pedidos"].sum().reset_index()
                if len(df_hor) > 0:
                    df_hor_piv = df_hor.pivot(index="horario", columns="periodo_semana", values="pedidos").fillna(0)
                    fig_hor = go.Figure(data=go.Heatmap(z=df_hor_piv.values, x=df_hor_piv.columns.tolist(), y=df_hor_piv.index.tolist(), colorscale=[[0,"#F5F0E8"],[0.5,"#B8923A"],[1,VERDE]], texttemplate="%{z:.0f}", textfont=dict(family="Nunito", size=11)))
                    fig_hor.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10), xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"), height=380, coloraxis_showscale=False)
                    st.plotly_chart(fig_hor, use_container_width=True, key="fig_hor_v")
        with col_h2:
            with st.container(border=True):
                st.markdown('<div class="section-title">Dias de Pico</div>', unsafe_allow_html=True)
                ordem_dias = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]
                df_dias = df_ifood_dias[df_ifood_dias["periodo"] == periodo_sel_v].copy()
                df_dias["dia_norm"] = df_dias["dia_semana"].str.normalize("NFKD").str.encode("ascii","ignore").str.decode("ascii").str.strip()
                df_dias_g = df_dias.groupby("dia_norm")["pedidos"].sum().reset_index()
                df_dias_ord = [d for d in ordem_dias if d in df_dias_g["dia_norm"].values]
                df_dias_g = df_dias_g.set_index("dia_norm").reindex(df_dias_ord).reset_index()
                if len(df_dias_g) > 0:
                    fig_dias = go.Figure(go.Bar(x=df_dias_g["dia_norm"], y=df_dias_g["pedidos"], marker_color=VERDE, text=df_dias_g["pedidos"], textposition="outside", textfont=dict(family="Nunito", size=12, color=MARROM)))
                    fig_dias.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10), xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(showgrid=False, tickfont=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"), height=380)
                    st.plotly_chart(fig_dias, use_container_width=True, key="fig_dias_v")
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="section-title">Mix de Pagamento</div>', unsafe_allow_html=True)
            df_pag = df_ifood_pagamentos[df_ifood_pagamentos["periodo"] == periodo_sel_v].groupby("forma_pagamento")["pedidos"].sum().reset_index().sort_values("pedidos", ascending=False)
            if len(df_pag) > 0:
                fig_pag = go.Figure(go.Pie(labels=df_pag["forma_pagamento"], values=df_pag["pedidos"], hole=0.5, textinfo="label+percent", textfont=dict(family="Nunito", size=12), marker=dict(colors=[VERDE,"#B8923A","#3D7A5C","#7A3D3D","#3D5A7A","#7A5C3D","#5C7A3D","#7A6B3D"])))
                fig_pag.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10), legend=dict(font=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"), height=320)
                st.plotly_chart(fig_pag, use_container_width=True, key="fig_pag_v")
elif aba_sel == "OlivIA":
    import anthropic as _anthropic
    import json as _json
    with open("static/olivia_banner_final.png", "rb") as _f:
        import base64 as _b64
        _olivia_b64 = _b64.b64encode(_f.read()).decode()
    st.markdown(f'<img src="data:image/png;base64,{_olivia_b64}" style="width:100%;border-radius:16px;margin-bottom:20px;box-shadow:0 4px 20px rgba(0,0,0,0.15);" />', unsafe_allow_html=True)

    # Inicializar historico na sessao
    if "olivia_messages" not in st.session_state:
        st.session_state.olivia_messages = []

    # System prompt com schema completo do banco
    # Contexto dinamico com dados reais
    # Contexto dinamico com dados reais de todo o banco
    def _gerar_contexto_banco():
        try:
            import psycopg2 as _pg
            _conn = get_conn()
            _cur = _conn.cursor()

            # iFood
            _cur.execute("SELECT filial, periodo, SUM(faturamento) as fat, SUM(pedidos) as ped FROM ifood_vendas WHERE logistica = 'Entrega parceira' GROUP BY filial, periodo ORDER BY filial, periodo")
            _if = _cur.fetchall()

            # Vendas salao 2026
            _cur.execute("SELECT filial, EXTRACT(month FROM data::date) as mes, SUM(venda_salao) as salao, SUM(meta_venda) as budget FROM vendas_diarias WHERE EXTRACT(year FROM data::date) = 2026 GROUP BY filial, EXTRACT(month FROM data::date) ORDER BY filial, mes")
            _vd = _cur.fetchall()

            # Pesquisa GSS - ultimo periodo por filial
            _cur.execute("SELECT restaurant, periodo, overall_experience, value, service, taste, speed_of_service, clean FROM pesquisa_performance ORDER BY periodo DESC LIMIT 12")
            _gss = _cur.fetchall()

            # Reclamacoes resumo
            _cur.execute("SELECT unidade_curta, COUNT(*) as n, ROUND(AVG(avaliacao)::numeric,2) as nota, tema FROM (SELECT unidade_curta, avaliacao, tema FROM reclamacoes_buzzmonitor WHERE data >= '2026-01-01') t GROUP BY unidade_curta, tema ORDER BY unidade_curta, n DESC")
            _recl = _cur.fetchall()

            # Reviews resumo
            _cur.execute("SELECT plataforma, COUNT(*) as n, ROUND(AVG(nota)::numeric,2) as nota FROM reviews GROUP BY plataforma")
            _rev = _cur.fetchall()

            # Fila espera resumo
            _cur.execute("SELECT status, COUNT(*) as n, ROUND(AVG(duracao_minutos)::numeric,1) as espera_media FROM fila_espera WHERE dia_chegada >= '2026-01-01' GROUP BY status")
            _fila = _cur.fetchall()

            # Menu - ultima semana
            _cur.execute("SELECT item, type, number_of_checks, gross_sales, revenue_score FROM menu_analysis WHERE semana_ref = (SELECT MAX(semana_ref) FROM menu_analysis) ORDER BY revenue_score DESC LIMIT 20")
            _menu = _cur.fetchall()

            _cur.close(); _conn.close()
            _meses = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

            ctx = "\nDADOS REAIS ATUALIZADOS DO BANCO:\n"

            ctx += "\n--- iFOOD (Entrega parceira) por periodo ---\n"
            for r in _if:
                ctx += f"- {r[0].replace('Olive Garden - ','')} | {r[1]} | R$ {r[2]:,.0f} | {r[3]} ped\n".replace(",",".")

            ctx += "\n--- VENDA SALAO 2026 por mes ---\n"
            _fil_ant = ""
            for r in _vd:
                _fil = r[0].replace("Olive Garden - ","")
                if _fil != _fil_ant:
                    if _fil_ant: ctx += "\n"
                    ctx += f"- {_fil}: "
                    _fil_ant = _fil
                else:
                    ctx += " | "
                ctx += f"{_meses.get(int(r[1]),'?')} salao Rk/budget Rk"
            ctx += "\n"

            ctx += "\n--- PESQUISA GSS (ultimos periodos) ---\n"
            for r in _gss:
                ctx += f"- {r[0].replace('Olive Garden - ','')} | {r[1]} | ExpGeral:{r[2]:.1f} Valor:{r[3]:.1f} Atend:{r[4]:.1f} Sabor:{r[5]:.1f} Veloc:{r[6]:.1f} Limp:{r[7]:.1f}\n"

            ctx += "\n--- RECLAMACOES BUZZMONITOR 2026 ---\n"
            _recl_fil = {}
            for r in _recl:
                if r[0] not in _recl_fil:
                    _recl_fil[r[0]] = []
                _recl_fil[r[0]].append(f"{r[3]}:{r[1]}")
            for fil, temas in _recl_fil.items():
                ctx += f"- {fil}: {' | '.join(temas[:3])}\n"

            ctx += "\n--- REVIEWS PLATAFORMAS ---\n"
            for r in _rev:
                ctx += f"- {r[0]}: {r[1]} reviews | nota media {r[2]}\n"

            ctx += "\n--- FILA DE ESPERA 2026 ---\n"
            for r in _fila:
                ctx += f"- {r[0]}: {r[1]} ocorrencias | espera media {r[2]} min\n"

            ctx += "\n--- MENU INTELLIGENCE (ultima semana) ---\n"
            for r in _menu:
                ctx += f"- {r[0]} | {r[1]} | {r[2]} checks | R$ {r[3]:,.0f} | score {r[4]:.1f}\n".replace(",",".")

            ctx += "\nATENCAO: Se sua query retornar valores muito diferentes destes, ha erro no SQL.\n"
            ctx += "Para iFood consulte ifood_vendas diretamente sem JOIN com vendas_diarias.\n"
            return ctx
        except Exception as _e:
            return f"\n(Contexto indisponivel: {_e})\n"
    _contexto_dinamico = _gerar_contexto_banco()

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
Regras SQL importantes para PostgreSQL/Supabase:
- Use ROUND(valor::numeric, 2) para arredondamento — NUNCA ROUND(double_precision, integer)
- Para percentuais: ROUND((a::numeric / NULLIF(b::numeric,0)) * 100, 1)
- Datas: EXTRACT(year FROM data), EXTRACT(month FROM data)
- Filiais sempre com nome completo: "Olive Garden - Morumbi" etc
- Para YTD 2026: WHERE EXTRACT(year FROM data) = 2026
- Para mes corrente: WHERE EXTRACT(month FROM data) = 6 AND EXTRACT(year FROM data) = 2026
- Sempre use aliases claros nas colunas (AS faturamento_total, etc)
- Limite resultados com LIMIT 50 quando nao for agregacao
- Para cruzar vendas_diarias com ifood_vendas, use EXTRACT(month FROM data) para o mes de vendas_diarias e extraia o mes do campo periodo de ifood_vendas com EXTRACT(month FROM TO_DATE(SPLIT_PART(periodo, ' - ', 1), 'DD/MM/YYYY'))
- O campo mes em vendas_diarias e VARCHAR (ex: "jan", "fev") — nunca faca join direto com numeros
- Para cruzar por mes/ano entre tabelas, sempre use EXTRACT nas datas
- Exemplo de join correto entre vendas e ifood:
  SELECT EXTRACT(month FROM v.data) as mes_num, SUM(v.venda_salao) as salao, SUM(i.faturamento) as ifood
  FROM vendas_diarias v
  LEFT JOIN ifood_vendas i ON EXTRACT(month FROM TO_DATE(SPLIT_PART(i.periodo, ' - ', 1), 'DD/MM/YYYY')) = EXTRACT(month FROM v.data)
  AND i.logistica = 'Entrega parceira'
  WHERE EXTRACT(year FROM v.data) = 2026
  GROUP BY mes_num ORDER BY mes_num


VALORES REAIS DO BANCO (use como referencia para validar suas queries):
- Venda Salao YTD 2026 Morumbi: ~R$ 13.3M | Aricanduva: ~R$ 4.1M
- iFood YTD 2026 (Entrega parceira apenas): Morumbi R$ 446k | Aricanduva R$ 232k | Center Norte R$ 348k | Dom Pedro R$ 173k
- NUNCA some venda_salao como faturamento iFood — sao tabelas diferentes
- Para faturamento iFood use SEMPRE: SELECT SUM(faturamento) FROM ifood_vendas WHERE logistica = 'Entrega parceira'
- Para share iFood: faturamento_ifood / (venda_salao + faturamento_ifood) * 100
- ifood_vendas tem apenas 4 filiais: Morumbi, Center Norte, Dom Pedro, Aricanduva
- GRU2 e GRU3 NAO tem iFood — nunca inclua no calculo de share iFood
- Queries de share devem filtrar vendas_diarias apenas para as 4 filiais com iFood quando comparando com iFood

QUERY CORRETA para share iFood por filial YTD 2026:
SELECT
    i.filial,
    SUM(i.faturamento) as fat_ifood,
    SUM(v.venda_salao) as fat_salao,
    ROUND(SUM(i.faturamento)::numeric / NULLIF((SUM(i.faturamento) + SUM(v.venda_salao))::numeric, 0) * 100, 1) as share_ifood
FROM ifood_vendas i
JOIN vendas_diarias v ON v.filial = i.filial
    AND EXTRACT(month FROM TO_DATE(SPLIT_PART(i.periodo, ' - ', 1), 'DD/MM/YYYY')) = EXTRACT(month FROM v.data)
    AND EXTRACT(year FROM v.data) = 2026
WHERE i.logistica = 'Entrega parceira'
GROUP BY i.filial
ORDER BY share_ifood DESC

"""

    # Conexao ao banco para execucao de queries
    def _executar_query(sql):
        try:
            import psycopg2
            conn = get_conn_ro()
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
                        system=OLIVIA_SYSTEM + _contexto_dinamico,
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
                                        tabela += "| " + " | ".join([str(v) if v is not None else "\u2014" for v in row]) + " |\n"
                                    # Segunda chamada — analise com os dados
                                    messages_llm2 = messages_llm + [
                                        {"role": "assistant", "content": resposta1},
                                        {"role": "user", "content": "Aqui estao os dados retornados pelo banco:\n\n" + tabela + "\nAgora apresente a analise executiva completa com a tabela e insights."}
                                    ]
                                    resp2 = client.messages.create(
                                        model="claude-sonnet-4-6",
                                        max_tokens=2000,
                                        system=OLIVIA_SYSTEM + _contexto_dinamico,
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

elif aba_sel == "Analises":
    from datetime import timedelta
    import numpy as np

    st.markdown('''<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Inteligencia & Predicao</div>
    <div style="font-size:13px; color:#8B9A2E; letter-spacing:0.1em; margin-bottom:20px;">DRIVERS DE REPUTACAO, PROJECOES E RISCO PREDITIVO</div>''', unsafe_allow_html=True)

    # Dados base
    df_perf_c = df_perf[df_perf["restaurant"] != "nan"].copy()
    df_perf_c["filial_curta"] = df_perf_c["restaurant"].str.replace("Olive Garden - ", "", regex=False)
    df_perf_c["periodo_curto"] = df_perf_c["periodo"].str.extract(r"(FW\d+ to FW\d+)")
    gss_atual = df_perf_c.sort_values("periodo_curto").groupby("filial_curta").last().reset_index() if len(df_perf_c) > 0 else pd.DataFrame()
    df_rep = df[df["sentimento"].isin(["Positivo","Negativo","Neutro"])].copy()
    rep_pub = df_rep.groupby("filial").agg(nota_media=("nota", "mean"), pct_pos=("sentimento", lambda x: (x == "Positivo").sum() / len(x) * 100)).reset_index()
    rep_pub["score_externo"] = (((rep_pub["nota_media"] - 1) / 4) * 40 + rep_pub["pct_pos"] * 0.6).clip(0, 100).round(1)
    rep_pub["filial_curta"] = rep_pub["filial"].str.replace("Olive Garden - ", "", regex=False)


    # BLOCO 3 — Score Preditivo de Risco
    with st.container(border=True):
        st.markdown('<div class="section-title">Score Preditivo de Risco — Proximos 30 Dias</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px; color:#8B7A5A; margin-bottom:16px;">Combina tendencia de vendas, trajetoria GSS e sentimento publico para identificar filiais com risco de deterioracao antes que os indicadores lagging sinalizem. Quanto maior o score, maior o risco.</div>', unsafe_allow_html=True)

        with st.expander("Metodologia do Score Preditivo de Risco"):
            st.markdown("""
**O que e?** Um indice composto (0-100) que combina tres dimensoes de saude operacional para antecipar deterioracao antes que ela apareca nos indicadores tradicionais.

**Composicao:**
- **Tendencia de Vendas (50%)** — compara a media diaria das ultimas 8 semanas vs o mesmo periodo do ano anterior. Queda > 5% gera risco proporcional.
- **GSS Experiencia Interna (30%)** — usa o % de insatisfacao do periodo mais recente. Quanto menor o GSS, maior o risco.
- **Reputacao Publica (20%)** — complemento do indice de reputacao publico. Reputacao degradada amplifica o risco.

**Niveis de risco:**
- Score < 12 — BAIXO: operacao saudavel, monitoramento padrao
- Score 12-25 — MEDIO: atencao requerida, investigar causa raiz
- Score > 25 — ALTO: acao imediata, risco real de deterioracao acelerada

**Por que esses pesos?** Vendas e o indicador mais sensivel e de resposta mais rapida (dados diarios). GSS captura a experiencia antes que vire review publico. Reputacao e o mais lagging dos tres, por isso tem menor peso.

**Limitacoes:** base historica de ~17 meses — pesos e limiares serao refinados conforme mais dados acumulam. Nao prevê eventos externos (feriados, obras, eventos no shopping).
            """)
        @st.cache_data(ttl=3600)
        def carregar_vendas_risco():
            conn = get_conn()
            df_r = pd.read_sql("SELECT data, filial, venda_salao, venda_ano1 FROM vendas_diarias ORDER BY data", conn)
            conn.close()
            return df_r

        df_risco = carregar_vendas_risco()
        df_risco["data"] = pd.to_datetime(df_risco["data"])
        df_risco["filial_curta"] = df_risco["filial"].str.replace("Olive Garden - ", "", regex=False)
        hoje_r = df_risco["data"].max()

        scores_risco = []
        for filial in sorted(df_risco["filial_curta"].unique()):
            dff = df_risco[df_risco["filial_curta"] == filial].copy()
            ult8 = dff[(dff["data"] >= hoje_r - timedelta(days=56)) & (dff["venda_salao"] > 0) & (dff["venda_ano1"] > 0)]
            fator_venda = ult8["venda_salao"].sum() / ult8["venda_ano1"].sum() if len(ult8) > 0 and ult8["venda_ano1"].sum() > 0 else 1.0
            risco_venda = max(0, (1 - fator_venda) * 100)
            gss_row = gss_atual[gss_atual["filial_curta"] == filial] if len(gss_atual) > 0 else pd.DataFrame()
            risco_gss = max(0, 100 - gss_row["overall_experience"].values[0]) if len(gss_row) > 0 else 20
            rep_row = rep_pub[rep_pub["filial_curta"] == filial]
            risco_rep = max(0, 100 - rep_row["score_externo"].values[0]) if len(rep_row) > 0 else 20
            score_risco = (risco_venda * 0.5 + risco_gss * 0.3 + risco_rep * 0.2)
            nivel = "ALTO" if score_risco >= 25 else "MEDIO" if score_risco >= 12 else "BAIXO"
            cor_risco = VERMELHO if nivel == "ALTO" else "#B8923A" if nivel == "MEDIO" else "#2e6b3e"
            scores_risco.append({"filial": filial, "score": round(score_risco, 1), "nivel": nivel, "cor": cor_risco, "fator_venda": fator_venda, "risco_gss": risco_gss, "risco_rep": risco_rep})

        scores_risco = sorted(scores_risco, key=lambda x: x["score"], reverse=True)
        col_r1, col_r2 = st.columns([1, 2])
        with col_r1:
            for r in scores_risco:
                pct = min(int(r["score"] * 2), 100)
                st.markdown(f'''<div style="padding:10px 0; border-bottom:1px solid #e8ddc8;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <span style="font-size:12px; font-weight:700; color:#3D2B1F;">{r["filial"]}</span>
                        <span style="font-size:12px; font-weight:800; color:{r["cor"]};">{r["nivel"]} {r["score"]:.1f}</span>
                    </div>
                    <div style="background:#e8ddc8; border-radius:4px; height:6px; margin-bottom:4px;">
                        <div style="background:{r["cor"]}; width:{pct}%; height:6px; border-radius:4px;"></div>
                    </div>
                    <div style="font-size:10px; color:#8B7A5A;">Vendas vs ano ant: {(r["fator_venda"]-1)*100:+.1f}% | GSS risco: {r["risco_gss"]:.0f} | Rep risco: {r["risco_rep"]:.0f}</div>
                </div>''', unsafe_allow_html=True)
        with col_r2:
            fig_risco = go.Figure()
            fig_risco.add_trace(go.Bar(
                x=[r["filial"] for r in scores_risco],
                y=[r["score"] for r in scores_risco],
                marker_color=[r["cor"] for r in scores_risco],
                text=[f'{r["nivel"]}\n{r["score"]:.1f}' for r in scores_risco],
                textposition="outside",
                textfont=dict(family="Nunito", size=10, color=MARROM)
            ))
            fig_risco.add_hline(y=25, line_dash="dash", line_color=VERMELHO, annotation_text="Risco Alto", annotation_font=dict(family="Nunito", size=9, color=VERMELHO))
            fig_risco.add_hline(y=12, line_dash="dash", line_color="#B8923A", annotation_text="Risco Medio", annotation_font=dict(family="Nunito", size=9, color="#B8923A"))
            fig_risco.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=20,b=10,l=10,r=10),
                xaxis=dict(tickfont=dict(family="Nunito", size=10, color=MARROM)),
                yaxis=dict(title="Score de Risco", showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10), range=[0, 55]),
                font=dict(family="Nunito"), height=320, showlegend=False
            )
            st.plotly_chart(fig_risco, use_container_width=True, key="fig_score_risco")

    st.markdown("<br>", unsafe_allow_html=True)


    # BLOCO 6 — Projecao de Vendas 4 Semanas (Ensemble STL + Ano Anterior)
    with st.container(border=True):
        st.markdown('<div class="section-title">Projecao de Vendas — Proximas 4 Semanas</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px; color:#8B7A5A; margin-bottom:16px;">Modelo ensemble: STL (sazonalidade semanal + mensal + tendencia) combinado com ano anterior. Pesos calculados automaticamente por backtest de 3 janelas por filial. MAPE mediano da rede: ~20%.</div>', unsafe_allow_html=True)

        from datetime import timedelta

        @st.cache_data(ttl=3600)
        def carregar_vendas_projecao():
            conn = get_conn()
            df_p = pd.read_sql("SELECT data, filial, venda_salao, venda_ano1 FROM vendas_diarias ORDER BY data", conn)
            conn.close()
            return df_p

        df_proj = carregar_vendas_projecao()
        df_proj["data"] = pd.to_datetime(df_proj["data"])
        df_proj["filial_curta"] = df_proj["filial"].str.replace("Olive Garden - ", "", regex=False)
        df_proj["dow"] = df_proj["data"].dt.dayofweek
        df_proj["mes_num"] = df_proj["data"].dt.month
        df_proj = df_proj[df_proj["venda_salao"] > 0].copy()
        hoje_proj = df_proj["data"].max()
        inicio_proj = hoje_proj + timedelta(days=1)
        fim_proj = hoje_proj + timedelta(days=28)

        def calcular_pesos_auto(dff, hoje_p, janelas=[56, 84, 112]):
            mapes_stl, mapes_a1 = [], []
            for janela in janelas:
                corte = hoje_p - timedelta(days=janela)
                treino = dff[dff["data"] <= corte]
                teste = dff[(dff["data"] > corte) & (dff["data"] <= corte + timedelta(days=28))]
                if len(treino) < 60 or len(teste) == 0:
                    continue
                media_b = treino["venda_salao"].mean()
                f_dow = treino.groupby("dow")["venda_salao"].mean() / media_b
                f_mes = treino.groupby("mes_num")["venda_salao"].mean() / media_b
                t2 = treino.copy()
                t2["t"] = (t2["data"] - t2["data"].min()).dt.days
                coef = np.polyfit(t2["t"], t2["venda_salao"], 1)
                rec = treino[treino["data"] >= treino["data"].max() - timedelta(days=28)]
                f_rec = rec["venda_salao"].mean() / media_b if len(rec) > 0 else 1.0
                f_a1 = (treino["venda_salao"] / treino["venda_ano1"]).replace([np.inf,-np.inf], np.nan).dropna().median()
                e_stl, e_a1 = [], []
                for _, row in teste.iterrows():
                    t_d = (row["data"] - treino["data"].min()).days
                    p_stl = media_b * f_dow.get(row["dow"],1.0) * f_mes.get(row["mes_num"],1.0) * (1 + coef[0]*t_d/media_b) * f_rec
                    real = row["venda_salao"]
                    e_stl.append(abs(p_stl - real) / real * 100)
                    if pd.notna(row["venda_ano1"]) and row["venda_ano1"] > 0:
                        e_a1.append(abs(row["venda_ano1"]*f_a1 - real) / real * 100)
                if e_stl: mapes_stl.append(np.mean(e_stl))
                if e_a1: mapes_a1.append(np.mean(e_a1))
            if not mapes_stl or not mapes_a1:
                return 0.7, 0.3
            inv_stl = 1 / np.mean(mapes_stl)
            inv_a1 = 1 / np.mean(mapes_a1)
            peso_stl = inv_stl / (inv_stl + inv_a1)
            return peso_stl, 1 - peso_stl

        resultados_proj = []
        for filial in sorted(df_proj["filial_curta"].unique()):
            dff = df_proj[df_proj["filial_curta"] == filial].copy().sort_values("data")
            treino = dff[dff["data"] <= hoje_proj]
            if len(treino) < 60:
                continue
            peso_stl, peso_a1 = calcular_pesos_auto(dff, hoje_proj)
            media_base = treino["venda_salao"].mean()
            fator_dow = treino.groupby("dow")["venda_salao"].mean() / media_base
            fator_mes = treino.groupby("mes_num")["venda_salao"].mean() / media_base
            t2 = treino.copy()
            t2["t"] = (t2["data"] - t2["data"].min()).dt.days
            coef = np.polyfit(t2["t"], t2["venda_salao"], 1)
            recente = treino[treino["data"] >= hoje_proj - timedelta(days=28)]
            fator_rec = recente["venda_salao"].mean() / media_base if len(recente) > 0 else 1.0
            fator_rec = float(np.clip(fator_rec, 0.85, 1.15))
            ult12 = treino[treino["data"] >= hoje_proj - timedelta(days=84)]
            fator_a1_med = (treino["venda_salao"] / treino["venda_ano1"]).replace([np.inf,-np.inf], np.nan).dropna().median()
            desvio_dow = ult12.groupby("dow")["venda_salao"].std().to_dict()
            dias_proj = []
            for d in range(1, 29):
                data_d = inicio_proj + timedelta(days=d-1)
                dow_d = data_d.weekday()
                mes_d = data_d.month
                t_d = (data_d - treino["data"].min()).days
                p_stl = media_base * fator_dow.get(dow_d,1.0) * fator_mes.get(mes_d,1.0) * (1 + coef[0]*t_d/media_base) * fator_rec
                data_ano1 = data_d - timedelta(days=364)
                ano1_row = dff[dff["data"] == pd.Timestamp(data_ano1)]
                if len(ano1_row) > 0 and ano1_row["venda_salao"].values[0] > 0:
                    p_a1 = ano1_row["venda_salao"].values[0] * fator_a1_med
                    p_final = p_stl * peso_stl + p_a1 * peso_a1
                else:
                    p_final = p_stl
                desvio_d = desvio_dow.get(dow_d, p_final * 0.20)
                dias_proj.append({
                    "data_proj": data_d,
                    "dow": dow_d,
                    "mes": mes_d,
                    "projecao": max(p_final, 0),
                    "proj_low": max(p_final - desvio_d, 0),
                    "proj_high": p_final + desvio_d,
                    "semana": (d - 1) // 7 + 1
                })
            df_dias = pd.DataFrame(dias_proj)
            resultados_proj.append({
                "filial": filial,
                "peso_stl": peso_stl,
                "peso_a1": peso_a1,
                "df": df_dias
            })

        # Cards de resumo por filial
        cols_proj = st.columns(len(resultados_proj))
        for idx, res in enumerate(resultados_proj):
            total = res["df"]["projecao"].sum()
            low = res["df"]["proj_low"].sum()
            high = res["df"]["proj_high"].sum()
            peso_stl = res["peso_stl"]
            cor_f = VERDE if peso_stl >= 0.65 else "#B8923A"
            with cols_proj[idx]:
                st.markdown(f'''<div style="background:#3D2B1F; border-radius:10px; padding:14px; text-align:center; border-top:4px solid {cor_f}; margin-bottom:8px;">
                    <div style="font-size:9px; color:#D8CFC0; letter-spacing:2px; margin-bottom:6px;">{res["filial"].upper()}</div>
                    <div style="font-size:20px; font-weight:800; color:#F5F0E8; margin-bottom:4px;">R$ {total/1000:.0f}k</div>
                    <div style="font-size:10px; color:#D8CFC0; margin-bottom:6px;">[{low/1000:.0f}k — {high/1000:.0f}k]</div>
                    <div style="font-size:10px; color:#8B9A2E;">STL {peso_stl:.0%} / Ano Ant {res["peso_a1"]:.0%}</div>
                    </div>''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Grafico barras empilhadas por semana
        semanas_labels = []
        for s in [1,2,3,4]:
            d_ini = (inicio_proj + timedelta(days=(s-1)*7)).strftime("%d/%m")
            d_fim = (inicio_proj + timedelta(days=s*7-1)).strftime("%d/%m")
            semanas_labels.append(f"Sem {s}\n{d_ini}-{d_fim}")

        cores_filiais = ["#8B9A2E","#4D3321","#B8923A","#8B2E2E","#5C7A8B","#7A5C8B"]
        fig_proj = go.Figure()
        for i, res in enumerate(resultados_proj):
            proj_sem = res["df"].groupby("semana")["projecao"].sum().reindex([1,2,3,4]).fillna(0)
            fig_proj.add_trace(go.Bar(
                name=res["filial"],
                x=semanas_labels,
                y=proj_sem.values,
                marker_color=cores_filiais[i % len(cores_filiais)],
                text=[f"R$ {v/1000:.0f}k" for v in proj_sem.values],
                textposition="inside",
                textfont=dict(family="Nunito", size=10, color="white")
            ))
        fig_proj.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10,b=10,l=10,r=10),
            legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
            xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
            yaxis=dict(title="", showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10)),
            font=dict(family="Nunito"), height=360
        )
        st.plotly_chart(fig_proj, use_container_width=True, key="fig_proj_vendas")

        # Grafico de linha por filial com intervalo de confianca
        st.markdown('<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-top:8px; margin-bottom:8px;">Projecao diaria com intervalo de confianca</div>', unsafe_allow_html=True)
        filial_graf = st.selectbox("Filial:", [r["filial"] for r in resultados_proj], key="sel_proj_filial")
        res_sel = next(r for r in resultados_proj if r["filial"] == filial_graf)
        df_sel = res_sel["df"].sort_values("data_proj")
        fig_linha = go.Figure()
        fig_linha.add_trace(go.Scatter(x=df_sel["data_proj"], y=df_sel["proj_high"], mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
        fig_linha.add_trace(go.Scatter(x=df_sel["data_proj"], y=df_sel["proj_low"], mode="lines", line=dict(width=0), fill="tonexty", fillcolor="rgba(139,154,46,0.15)", showlegend=False, hoverinfo="skip"))
        fig_linha.add_trace(go.Scatter(
            x=df_sel["data_proj"], y=df_sel["projecao"], mode="lines+markers",
            line=dict(color=VERDE, width=2), marker=dict(size=6, color=VERDE),
            name="Projecao Ensemble",
            text=[f"R$ {v:,.0f}" for v in df_sel["projecao"]],
            hovertemplate="%{x|%d/%m}<br>%{text}<extra></extra>"
        ))
        fig_linha.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10,b=10,l=10,r=10),
            xaxis=dict(tickformat="%d/%m", tickfont=dict(family="Nunito", size=10, color=MARROM)),
            yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10), tickprefix="R$ "),
            legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
            font=dict(family="Nunito"), height=300
        )
        st.plotly_chart(fig_linha, use_container_width=True, key="fig_linha_proj")


elif aba_sel == "Menu":
    st.markdown('<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Menu Intelligence</div>', unsafe_allow_html=True)
    if len(df_menu) == 0:
        st.warning("Sem dados de menu. Rode importar_menu_analysis.py.")
    else:
        semanas_disp = sorted(df_menu["semana_ref"].unique(), reverse=True)
        semana_sel = semanas_disp[0]
        df_m = df_menu[df_menu["semana_ref"] == semana_sel].copy()
        df_m = df_m[~df_m["item"].str.upper().isin(["BROWNIE CORTESIA","SSB"])]
        df_m = df_m[~df_m["item"].str.upper().str.startswith("RF ")]
        df_m = df_m[df_m["type"].isin(["Star","Dog","Puzzle","Horse"])]

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            canal_sel = st.selectbox("Canal:", ["Ambos","POS","Delivery"], key="menu_canal")
        with col_f2:
            tipo_sel = st.selectbox("Tipo Boston:", ["Todos","Star","Dog","Puzzle","Horse"], key="menu_tipo")

        df_mf = df_m.copy()
        if canal_sel != "Ambos":
            df_mf = df_mf[df_mf["canal"] == canal_sel]
        if tipo_sel != "Todos":
            df_mf = df_mf[df_mf["type"] == tipo_sel]

        COR_BOSTON = {"Star": "#B8923A", "Dog": VERMELHO, "Puzzle": "#4A90D9", "Horse": VERDE}
        stars = df_mf[df_mf["type"]=="Star"]
        dogs = df_mf[df_mf["type"]=="Dog"]
        puzzles = df_mf[df_mf["type"]=="Puzzle"]
        horses = df_mf[df_mf["type"]=="Horse"]
        gross_total = df_mf["gross_sales"].sum() if df_mf["gross_sales"].sum() > 0 else 1
        df_bebs = df_mf[df_mf["item"].str.upper().str.contains("SCHW TONICA|SCHW CITRUS|FANTA GUARANA", na=False)]
        qty_bebs = df_bebs["quantity_per_check"].mean() if len(df_bebs) > 0 else 0
        uplift_medio = df_mf[df_mf["check_uplift"].notna()]["check_uplift"].mean() if df_mf["check_uplift"].notna().any() else 0

        st.markdown(f'<div style="font-size:11px; color:#8B7A5A; margin-bottom:16px;">Referencia: {semana_sel} | {len(semanas_disp)} semana(s) de historico</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 1 — KPIs
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        with col_k1:
            with st.container(border=True):
                st.markdown('<div style="text-align:center;padding:8px;"><div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:4px;">GROSS SALES</div>' + f'<div style="font-size:24px;font-weight:500;color:#3D2B1F;">R$ {"  {:,.0f}".format(gross_total).replace(",",".")}</div>' + f'<div style="font-size:10px;color:#8B9A2E;">{stars["gross_sales"].sum()/gross_total*100:.0f}% Stars</div></div>', unsafe_allow_html=True)
        with col_k2:
            with st.container(border=True):
                pct_star_mix = stars["number_of_checks"].sum()/df_mf["number_of_checks"].sum()*100 if df_mf["number_of_checks"].sum()>0 else 0
                st.markdown('<div style="text-align:center;padding:8px;"><div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:4px;">STARS NO MIX</div>' + f'<div style="font-size:24px;font-weight:500;color:#B8923A;">{len(stars)} itens</div>' + f'<div style="font-size:10px;color:#8B7A5A;">{pct_star_mix:.0f}% dos checks</div></div>', unsafe_allow_html=True)
        with col_k3:
            with st.container(border=True):
                pct_puz_mix = puzzles["number_of_checks"].sum()/df_mf["number_of_checks"].sum()*100 if df_mf["number_of_checks"].sum()>0 else 0
                st.markdown('<div style="text-align:center;padding:8px;"><div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:4px;">PUZZLES</div>' + f'<div style="font-size:24px;font-weight:500;color:#4A90D9;">{len(puzzles)} itens</div>' + f'<div style="font-size:10px;color:#8B7A5A;">{pct_puz_mix:.0f}% dos checks</div></div>', unsafe_allow_html=True)
        with col_k4:
            with st.container(border=True):
                cor_up = "#2e6b3e" if uplift_medio > 100 else "#B8923A"
                st.markdown('<div style="text-align:center;padding:8px;"><div style="font-size:9px;color:#8B7A5A;letter-spacing:2px;margin-bottom:4px;">CHECK UPLIFT MEDIO</div>' + f'<div style="font-size:24px;font-weight:500;color:{cor_up};">R$ {uplift_medio:.0f}</div>' + '<div style="font-size:10px;color:#8B7A5A;">valor extra por check</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 2 — TOP 5 POR TIPO
        with st.container(border=True):
            st.markdown('<div class="section-title">Top 5 por Tipo Boston</div>', unsafe_allow_html=True)
            col_s, col_h, col_p, col_d = st.columns(4)
            for col_t, tipo, label in [(col_s,"Star","⭐ Stars"),(col_h,"Horse","🐴 Horses"),(col_p,"Puzzle","🔵 Puzzles"),(col_d,"Dog","🔴 Dogs")]:
                df_tipo = df_mf[df_mf["type"]==tipo].sort_values("gross_sales", ascending=False).head(5)
                cor = COR_BOSTON.get(tipo, MARROM)
                with col_t:
                    st.markdown(f'<div style="font-size:11px;font-weight:700;color:{cor};margin-bottom:8px;">{label}</div>', unsafe_allow_html=True)
                    if len(df_tipo) == 0:
                        st.markdown('<div style="font-size:11px;color:#8B7A5A;">Sem itens</div>', unsafe_allow_html=True)
                    for _, r in df_tipo.iterrows():
                        gs = "R$ {:,.0f}".format(r["gross_sales"]).replace(",",".")
                        st.markdown(
                            f'<div style="padding:6px 0;border-bottom:1px solid #e8ddc8;">' +
                            f'<div style="font-size:11px;font-weight:500;color:#3D2B1F;">{r["item"][:28]}</div>' +
                            f'<div style="font-size:10px;color:#8B7A5A;">{gs} | {int(r["number_of_checks"])} checks</div></div>',
                            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 3 — TABELA COMPLETA
        with st.container(border=True):
            st.markdown('<div class="section-title">Todos os Itens</div>', unsafe_allow_html=True)
            df_tab = df_mf[["item","type","canal","gross_sales","number_of_checks","ct_gross_total_check_avg","check_uplift"]].copy()
            df_tab = df_tab.sort_values("gross_sales", ascending=False)
            df_tab["gross_sales"] = df_tab["gross_sales"].apply(lambda v: "R$ {:,.0f}".format(v).replace(",",".") if pd.notna(v) else "—")
            df_tab["ct_gross_total_check_avg"] = df_tab["ct_gross_total_check_avg"].apply(lambda v: f"R$ {v:.0f}" if pd.notna(v) else "—")
            df_tab["check_uplift"] = df_tab["check_uplift"].apply(lambda v: f"R$ {v:.0f}" if pd.notna(v) else "—")
            df_tab["number_of_checks"] = df_tab["number_of_checks"].apply(lambda v: f"{int(v):,}".replace(",",".") if pd.notna(v) else "—")
            df_tab.columns = ["Item","Tipo","Canal","Gross Sales","Checks","Check Completo","Uplift"]
            st.dataframe(df_tab, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 3b — MATRIZ DE CRUZAMENTO
        with st.container(border=True):
            st.markdown('<div class="section-title">Matriz de Cruzamento — Uplift vs Volume</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px; color:#8B7A5A; margin-bottom:12px;">Eixo X = volume de checks | Eixo Y = Check Uplift (R$) | Tamanho = Impacto Total (Uplift x Checks) | Cor = Tipo Boston</div>', unsafe_allow_html=True)
            df_matriz = df_mf.copy()
            df_matriz["uplift_calc"] = df_matriz["ct_gross_total_check_avg"] - df_matriz["gross_total_check_avg"]
            df_matriz["impacto_total"] = df_matriz["uplift_calc"] * df_matriz["number_of_checks"]
            df_matriz = df_matriz.dropna(subset=["uplift_calc","number_of_checks","impacto_total"])
            if len(df_matriz) > 0:
                med_up = df_matriz["uplift_calc"].median()
                med_ch = df_matriz["number_of_checks"].median()
                fig_mat = go.Figure()
                for tipo in ["Star","Dog","Puzzle","Horse"]:
                    dft = df_matriz[df_matriz["type"]==tipo]
                    if len(dft) == 0:
                        continue
                    tamanho = dft["impacto_total"].apply(lambda v: max(8, min(50, abs(v)/50000)))
                    fig_mat.add_trace(go.Scatter(
                        x=dft["number_of_checks"],
                        y=dft["uplift_calc"],
                        mode="markers",
                        name=tipo,
                        marker=dict(size=tamanho, color=COR_BOSTON.get(tipo, MARROM), opacity=0.75, line=dict(width=1, color="white")),
                        hovertemplate="<b>%{customdata[0]}</b><br>Checks: %{x}<br>Uplift: R$ %{y:.0f}<br>Impacto: R$ %{customdata[1]:,.0f}<extra></extra>",
                        customdata=list(zip(dft["item"].str[:30], dft["impacto_total"]))
                    ))
                fig_mat.add_vline(x=med_ch, line_dash="dot", line_color="#8B7A5A", line_width=1)
                fig_mat.add_hline(y=med_up, line_dash="dot", line_color="#8B7A5A", line_width=1)
                anotacoes = [
                    dict(x=df_matriz["number_of_checks"].max()*0.85, y=df_matriz["uplift_calc"].max()*0.90, text="Prioridade 1 — Proteger", showarrow=False, font=dict(size=9, color="#2e6b3e")),
                    dict(x=df_matriz["number_of_checks"].min()*1.5, y=df_matriz["uplift_calc"].max()*0.90, text="Promover — Aumentar visibilidade", showarrow=False, font=dict(size=9, color="#4A90D9")),
                    dict(x=df_matriz["number_of_checks"].max()*0.85, y=df_matriz["uplift_calc"].min()*0.90, text="Revisar preco", showarrow=False, font=dict(size=9, color="#B8923A")),
                    dict(x=df_matriz["number_of_checks"].min()*1.5, y=df_matriz["uplift_calc"].min()*0.90, text="Avaliar — Monitorar ou cortar", showarrow=False, font=dict(size=9, color=VERMELHO)),
                ]
                fig_mat.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=40,l=60,r=10),
                    xaxis=dict(title="Numero de Checks", showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                    yaxis=dict(title="Check Uplift (R$)", showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                    legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                    annotations=anotacoes,
                    font=dict(family="Nunito"), height=420
                )
                st.plotly_chart(fig_mat, use_container_width=True, key="fig_matriz_menu")
                col_q1, col_q2, col_q3, col_q4 = st.columns(4)
                for col_q, q_label, q_cor, q_desc, q_fn in [
                    (col_q1, "Prioridade 1", "#2e6b3e", "Proteger e impulsionar", lambda r: r["uplift_calc"]>=med_up and r["number_of_checks"]>=med_ch),
                    (col_q2, "Promover", "#4A90D9", "Aumentar visibilidade", lambda r: r["uplift_calc"]>=med_up and r["number_of_checks"]<med_ch),
                    (col_q3, "Revisar preco", "#B8923A", "Avaliar precificacao", lambda r: r["uplift_calc"]<med_up and r["number_of_checks"]>=med_ch),
                    (col_q4, "Avaliar", VERMELHO, "Monitorar ou cortar", lambda r: r["uplift_calc"]<med_up and r["number_of_checks"]<med_ch),
                ]:
                    df_q = df_matriz[df_matriz.apply(q_fn, axis=1)]
                    with col_q:
                        itens_html = "".join([f'<div style="font-size:10px;color:#3D2B1F;padding:2px 0;border-bottom:1px solid #e8ddc8;">{r["item"][:22]}</div>' for _, r in df_q.head(5).iterrows()])
                        extra = f'<div style="font-size:9px;color:#8B7A5A;margin-top:4px;">+{len(df_q)-5} itens</div>' if len(df_q)>5 else ""
                        st.markdown(
                            f'<div style="background:#F5F0E8;border-radius:8px;padding:10px;border-left:3px solid {q_cor};">' +
                            f'<div style="font-size:10px;font-weight:700;color:{q_cor};margin-bottom:4px;">{q_label}</div>' +
                            f'<div style="font-size:9px;color:#8B7A5A;margin-bottom:6px;">{q_desc}</div>' +
                            itens_html + extra + '</div>',
                            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 4 — BEBIDAS PUZZLE
        with st.container(border=True):
            st.markdown('<div class="section-title">Bebidas Puzzle — Script de Sugestao Ativa</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;color:#8B7A5A;margin-bottom:12px;">Schw Tonica + Schw Citrus + Fanta Guarana. Baseline: 1,11 un/check | Meta: 1,50 un/check.</div>', unsafe_allow_html=True)
            baseline_beb = 1.11
            meta_beb = 1.50
            pct_g = min((qty_bebs-baseline_beb)/(meta_beb-baseline_beb)*100,100) if qty_bebs>baseline_beb else 0
            cor_g = "#2e6b3e" if qty_bebs>=meta_beb else "#B8923A" if qty_bebs>=baseline_beb else VERMELHO
            status_g = "Meta atingida!" if qty_bebs>=meta_beb else f"Faltam {meta_beb-qty_bebs:.2f} un/check para a meta"
            col_g1, col_g2 = st.columns([1,2])
            with col_g1:
                st.markdown(
                    f'<div style="text-align:center;padding:20px;">' +
                    f'<div style="font-size:56px;font-weight:800;color:{cor_g};line-height:1;">{qty_bebs:.2f}</div>' +
                    f'<div style="font-size:11px;color:#8B7A5A;margin:6px 0;">un/check atual</div>' +
                    f'<div style="background:#e8ddc8;border-radius:8px;height:10px;margin:12px 0;">' +
                    f'<div style="background:{cor_g};width:{max(pct_g,3):.0f}%;height:10px;border-radius:8px;"></div></div>' +
                    f'<div style="display:flex;justify-content:space-between;font-size:10px;color:#8B7A5A;">' +
                    f'<span>Baseline: {baseline_beb}</span><span>Meta: {meta_beb}</span></div>' +
                    f'<div style="font-size:12px;font-weight:500;color:{cor_g};margin-top:8px;">{status_g}</div></div>',
                    unsafe_allow_html=True)
            with col_g2:
                if len(df_bebs) > 0:
                    for _, r in df_bebs.iterrows():
                        cor_b = "#2e6b3e" if r["quantity_per_check"] >= meta_beb else "#B8923A" if r["quantity_per_check"] >= baseline_beb else VERMELHO
                        st.markdown(
                            f'<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #e8ddc8;">' +
                            f'<div style="font-size:12px;font-weight:500;color:#3D2B1F;">{r["item"]}</div>' +
                            f'<div style="font-size:12px;font-weight:700;color:{cor_b};">{r["quantity_per_check"]:.2f} un/check</div>' +
                            f'<div style="font-size:11px;color:#8B7A5A;">{int(r["number_of_checks"])} checks</div></div>',
                            unsafe_allow_html=True)
                else:
                    st.markdown('<div style="font-size:12px;color:#8B7A5A;padding:20px;">Bebidas Puzzle nao encontradas nos dados filtrados.</div>', unsafe_allow_html=True)


elif aba_sel == "Fila":
    st.markdown('<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Fila de Espera</div>', unsafe_allow_html=True)

    if len(df_fila) == 0:
        st.warning("Sem dados de fila. Rode importar_fila_espera.py.")
    else:
        df_fe = df_fila.copy()
        df_fe["dia_chegada"] = pd.to_datetime(df_fe["dia_chegada"])
        df_fe["dow"] = df_fe["dia_chegada"].dt.dayofweek
        df_fe["mes"] = df_fe["dia_chegada"].dt.to_period("M").astype(str)
        df_fe["hora_num"] = df_fe["hora_chegada"].apply(lambda x: int(str(x)[:2]) if pd.notna(x) else None)
        df_fe["turno"] = df_fe["hora_num"].apply(lambda h: "Almoco" if h and 11<=h<=15 else "Jantar" if h and 16<=h<=22 else "Outros")
        dias_label = {0:"Seg",1:"Ter",2:"Qua",3:"Qui",4:"Sex",5:"Sab",6:"Dom"}

        # Filtros
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            meses_disp = ["Todos"] + sorted(df_fe["mes"].unique().tolist())
            mes_sel_f = st.selectbox("Mes:", meses_disp, key="fila_mes")
        with col_f2:
            status_disp = ["Todos"] + sorted(df_fe["status"].dropna().unique().tolist())
            status_sel_f = st.selectbox("Status:", status_disp, key="fila_status")
        with col_f3:
            unid_disp = ["Todas"] + sorted(df_fe["unidade"].dropna().unique().tolist()) if df_fe["unidade"].notna().any() else ["Todas"]
            unid_sel_f = st.selectbox("Unidade:", unid_disp, key="fila_unidade")

        df_ff = df_fe.copy()
        if mes_sel_f != "Todos":
            df_ff = df_ff[df_ff["mes"] == mes_sel_f]
        if status_sel_f != "Todos":
            df_ff = df_ff[df_ff["status"] == status_sel_f]
        if unid_sel_f != "Todas":
            df_ff = df_ff[df_ff["unidade"] == unid_sel_f]

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 1 — KPIs
        with st.container(border=True):
            st.markdown('<div class="section-title">Resumo Executivo</div>', unsafe_allow_html=True)
            total = len(df_ff)
            sentados = len(df_ff[df_ff["status"]=="Sentado"])
            cancelados = len(df_ff[df_ff["status"].str.contains("Cancelado", na=False)])
            noshow = len(df_ff[df_ff["status"].str.contains("no-show", case=False, na=False)])
            tx_conv = sentados/total*100 if total>0 else 0
            espera_media = df_ff[df_ff["status"]=="Sentado"]["duracao_minutos"].mean()
            grupo_medio = df_ff["pessoas"].mean()
            col_k1,col_k2,col_k3,col_k4,col_k5,col_k6 = st.columns(6)
            with col_k1: st.metric("Total Filas", total)
            with col_k2:
                cor_conv = "#2e6b3e" if tx_conv>=80 else "#B8923A" if tx_conv>=60 else VERMELHO
                st.markdown(f'<div style="text-align:center;"><div style="font-size:12px;color:#8B7A5A;">Taxa Conversao</div><div style="font-size:24px;font-weight:700;color:{cor_conv};">{tx_conv:.1f}%</div></div>', unsafe_allow_html=True)
            with col_k3: st.metric("Sentados", sentados)
            with col_k4: st.metric("Cancelamentos", cancelados)
            with col_k5: st.metric("No-show", noshow)
            with col_k6:
                cor_esp = "#2e6b3e" if pd.notna(espera_media) and espera_media<=15 else "#B8923A" if pd.notna(espera_media) and espera_media<=30 else VERMELHO
                st.markdown(f'<div style="text-align:center;"><div style="font-size:12px;color:#8B7A5A;">Espera Media</div><div style="font-size:24px;font-weight:700;color:{cor_esp};">{espera_media:.0f} min</div></div>' if pd.notna(espera_media) else '<div style="text-align:center;"><div style="font-size:12px;color:#8B7A5A;">Espera Media</div><div style="font-size:24px;font-weight:700;color:#8B7A5A;">—</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 2 — CONVERSAO E ESPERA
        with st.container(border=True):
            st.markdown('<div class="section-title">Conversao e Tempo de Espera</div>', unsafe_allow_html=True)
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Status da Fila</div>', unsafe_allow_html=True)
                status_cnt = df_ff["status"].value_counts().reset_index()
                status_cnt.columns = ["status","n"]
                cores_status = {"Sentado":"#2e6b3e","Cancelado por solicitação do cliente":"#B8923A","Cancelado pelo cliente":VERMELHO,"Cancelado por no-show do cliente":"#8B7A5A"}
                fig_status = go.Figure(go.Pie(
                    labels=status_cnt["status"], values=status_cnt["n"],
                    marker_colors=[cores_status.get(s, MARROM) for s in status_cnt["status"]],
                    hole=0.4, textfont=dict(family="Nunito", size=11)
                ))
                fig_status.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10,l=10,r=10),
                    legend=dict(font=dict(family="Nunito", size=9, color=MARROM)), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_status, use_container_width=True, key="fig_status_fila")
            with col_c2:
                st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Distribuicao do Tempo de Espera (Sentados)</div>', unsafe_allow_html=True)
                df_sent = df_ff[df_ff["status"]=="Sentado"]["duracao_minutos"].dropna()
                fig_hist = go.Figure(go.Histogram(
                    x=df_sent, nbinsx=20,
                    marker_color=VERDE, opacity=0.8
                ))
                fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(title="Minutos", tickfont=dict(family="Nunito", size=10, color=MARROM)),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10)),
                    font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_hist, use_container_width=True, key="fig_hist_fila")

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 3 — HEATMAP HORA x DIA
        with st.container(border=True):
            st.markdown('<div class="section-title">Heatmap — Volume de Filas por Hora e Dia</div>', unsafe_allow_html=True)
            df_heat = df_ff.dropna(subset=["hora_num","dow"]).copy()
            df_heat["dow_label"] = df_heat["dow"].map(dias_label)
            pivot_heat = df_heat.groupby(["hora_num","dow"]).size().reset_index(name="n")
            if len(pivot_heat) > 0:
                pivot_m = pivot_heat.pivot(index="hora_num", columns="dow", values="n").fillna(0)
                pivot_m.columns = [dias_label.get(c,c) for c in pivot_m.columns]
                fig_heat = go.Figure(data=go.Heatmap(
                    z=pivot_m.values,
                    x=pivot_m.columns.tolist(),
                    y=[f"{h}h" for h in pivot_m.index.tolist()],
                    colorscale=[[0,"#F5F0E8"],[0.5,"#B8923A"],[1,VERDE]],
                    texttemplate="%{z:.0f}",
                    textfont=dict(family="Nunito", size=10)
                ))
                fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    font=dict(family="Nunito"), height=380, coloraxis_showscale=False)
                st.plotly_chart(fig_heat, use_container_width=True, key="fig_heat_fila")

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 4 — ESPERA POR DIA E TURNO
        with st.container(border=True):
            st.markdown('<div class="section-title">Tempo Medio de Espera por Dia e Turno</div>', unsafe_allow_html=True)
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Por Dia da Semana</div>', unsafe_allow_html=True)
                df_sent2 = df_ff[df_ff["status"]=="Sentado"].copy()
                esp_dow = df_sent2.groupby("dow")["duracao_minutos"].mean().reset_index()
                esp_dow["label"] = esp_dow["dow"].map(dias_label)
                esp_dow = esp_dow.sort_values("dow")
                fig_dow = go.Figure(go.Bar(
                    x=esp_dow["label"], y=esp_dow["duracao_minutos"],
                    marker_color=[VERDE if v<=15 else "#B8923A" if v<=30 else VERMELHO for v in esp_dow["duracao_minutos"]],
                    text=esp_dow["duracao_minutos"].apply(lambda v: f"{v:.0f} min"),
                    textposition="outside", textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_dow.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_dow, use_container_width=True, key="fig_dow_fila")
            with col_d2:
                st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Por Turno</div>', unsafe_allow_html=True)
                esp_turno = df_sent2.groupby("turno")["duracao_minutos"].agg(["mean","count"]).reset_index()
                esp_turno.columns = ["turno","media","n"]
                fig_turno_f = go.Figure(go.Bar(
                    x=esp_turno["turno"], y=esp_turno["media"],
                    marker_color=[VERDE, "#B8923A", "#8B7A5A"][:len(esp_turno)],
                    text=esp_turno["media"].apply(lambda v: f"{v:.0f} min"),
                    textposition="outside", textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_turno_f.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_turno_f, use_container_width=True, key="fig_turno_fila")

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 5 — TAMANHO DO GRUPO
        with st.container(border=True):
            st.markdown('<div class="section-title">Tamanho do Grupo</div>', unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Distribuicao por Numero de Pessoas</div>', unsafe_allow_html=True)
                grupo_cnt = df_ff["pessoas"].value_counts().sort_index().reset_index()
                grupo_cnt.columns = ["pessoas","n"]
                fig_grupo = go.Figure(go.Bar(
                    x=grupo_cnt["pessoas"].astype(str)+"p",
                    y=grupo_cnt["n"],
                    marker_color=VERDE,
                    text=grupo_cnt["n"], textposition="outside",
                    textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_grupo.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=False), font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_grupo, use_container_width=True, key="fig_grupo_fila")
            with col_g2:
                st.markdown('<div style="font-size:11px;font-weight:700;color:#8B9A2E;margin-bottom:8px;">Espera Media por Tamanho de Grupo</div>', unsafe_allow_html=True)
                esp_grupo = df_ff[df_ff["status"]=="Sentado"].groupby("pessoas")["duracao_minutos"].mean().reset_index()
                fig_esp_g = go.Figure(go.Scatter(
                    x=esp_grupo["pessoas"], y=esp_grupo["duracao_minutos"],
                    mode="lines+markers+text",
                    line=dict(color="#B8923A", width=2),
                    marker=dict(size=8, color="#B8923A"),
                    text=esp_grupo["duracao_minutos"].apply(lambda v: f"{v:.0f}min"),
                    textposition="top center",
                    textfont=dict(family="Nunito", size=10, color=MARROM)
                ))
                fig_esp_g.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10,b=10,l=10,r=10),
                    xaxis=dict(title="Pessoas", tickfont=dict(family="Nunito", size=11, color=MARROM)),
                    yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10)),
                    font=dict(family="Nunito"), height=260)
                st.plotly_chart(fig_esp_g, use_container_width=True, key="fig_esp_grupo_fila")

        st.markdown("<br>", unsafe_allow_html=True)

        # BLOCO 6 — EVOLUCAO MENSAL
        with st.container(border=True):
            st.markdown('<div class="section-title">Evolucao Mensal</div>', unsafe_allow_html=True)
            evo_mes = df_fe.groupby("mes").agg(
                total=("status","count"),
                sentados=("status", lambda x: (x=="Sentado").sum()),
                espera=("duracao_minutos","mean")
            ).reset_index()
            evo_mes["tx_conv"] = evo_mes["sentados"]/evo_mes["total"]*100
            fig_evo_f = go.Figure()
            fig_evo_f.add_trace(go.Bar(x=evo_mes["mes"], y=evo_mes["total"], name="Total Filas", marker_color="#8B7A5A", opacity=0.6))
            fig_evo_f.add_trace(go.Bar(x=evo_mes["mes"], y=evo_mes["sentados"], name="Sentados", marker_color=VERDE))
            fig_evo_f.add_trace(go.Scatter(x=evo_mes["mes"], y=evo_mes["tx_conv"], name="Taxa Conv. %",
                mode="lines+markers", line=dict(color="#B8923A", width=2), marker=dict(size=8),
                yaxis="y2"))
            fig_evo_f.update_layout(
                barmode="overlay",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10,b=10,l=10,r=60),
                xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM), showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E8DCC8", tickfont=dict(family="Nunito", size=10)),
                yaxis2=dict(overlaying="y", side="right", ticksuffix="%", showgrid=False, tickfont=dict(family="Nunito", size=10, color="#B8923A")),
                legend=dict(font=dict(family="Nunito", size=10, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
                font=dict(family="Nunito"), height=320
            )
            st.plotly_chart(fig_evo_f, use_container_width=True, key="fig_evo_fila")

st.markdown(
    '<div style="text-align:center; font-size:10px; color:#B8A898; letter-spacing:0.1em; padding-top:20px;">'
    'OLIVE GARDEN BRAND INTELLIGENCE © 2026</div>',
    unsafe_allow_html=True
)





