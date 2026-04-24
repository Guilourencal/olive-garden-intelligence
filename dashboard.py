import streamlit as st
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
                if senha == os.getenv("DASHBOARD_PASSWORD", "olivegarden2026"):
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
[data-testid="stSidebar"] { background-color: #4D3321; border-right: 3px solid #8B9A2E; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: #D8CFC0 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background-color: #5a3f2a; color: #F5F0E8; border: 1px solid #8B9A2E; border-radius: 6px; }
[data-testid="stSidebar"] button { border-radius: 20px !important; border: 1px solid rgba(255,255,255,0.15) !important; background: rgba(255,255,255,0.08) !important; color: #D8CFC0 !important; font-size: 13px !important; font-weight: 600 !important; letter-spacing: 0.05em !important; margin-bottom: 4px !important; }
[data-testid="stSidebar"] button:hover { background: rgba(139,154,46,0.3) !important; color: white !important; border-color: #8B9A2E !important; }
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

def get_conn():
    return psycopg2.connect(
        host="aws-1-sa-east-1.pooler.supabase.com",
        port=6543,
        user="postgres.rvauallshhozpruvusrr",
        password="olivegarden2233@",
        database="postgres"
    )

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

@st.cache_data(ttl=3600)
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

df = carregar_reviews()
df_social = carregar_social()
df_news = carregar_noticias()
df_comments = carregar_pesquisa_comments()
df_perf = carregar_pesquisa_performance()

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

    for aba in ["Reviews", "Social", "Notícias", "Pesquisa", "OlivIA"]:
        if st.button(aba, key=f"btn_{aba}", use_container_width=True):
            st.session_state.aba_sel = aba
            st.rerun()

    aba_sel = st.session_state.aba_sel

    st.markdown('<div style="height:1px; background:rgba(255,255,255,0.1); margin:10px 0;"></div>', unsafe_allow_html=True)

    sent_social_sel = "Todos"
    post_sel = "Todos"
    cat_sel = "Todas"
    periodo_sel = "Últimos 30 dias"
    idioma_sel = "Todos"
    plataforma_sel = "Todas"
    filial_sel = "Todas"
    sentimento_sel = "Todos"

    if aba_sel == "Reviews":
        st.markdown('<div class="sidebar-label">Plataforma</div>', unsafe_allow_html=True)
        plataformas = ["Todas"] + sorted(df["plataforma"].dropna().unique().tolist())
        plataforma_sel = st.selectbox("Plataforma", plataformas, key="plat", label_visibility="collapsed")
        st.markdown('<div class="sidebar-label">Filial</div>', unsafe_allow_html=True)
        filiais = ["Todas"] + sorted(df["filial"].dropna().unique().tolist())
        filial_sel = st.selectbox("Filial", filiais, key="filial", label_visibility="collapsed")
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
    df_f = df.copy()
    if plataforma_sel != "Todas":
        df_f = df_f[df_f["plataforma"] == plataforma_sel]
    if filial_sel != "Todas":
        df_f = df_f[df_f["filial"] == filial_sel]
    if sentimento_sel != "Todos":
        df_f = df_f[df_f["sentimento"] == sentimento_sel]

    data_coleta_max = pd.to_datetime(df_f["data_coleta"], errors="coerce").max()
    data_coleta_str = data_coleta_max.strftime("%d/%m/%Y %H:%M") if pd.notna(data_coleta_max) else "—"
    data_review_min = pd.to_datetime(df_f["data_original"], errors="coerce", utc=True).min()
    data_review_max = pd.to_datetime(df_f["data_original"], errors="coerce", utc=True).max()
    if pd.notna(data_review_min) and pd.notna(data_review_max):
        periodo_str = f"{data_review_min.strftime('%d/%m/%Y')} a {data_review_max.strftime('%d/%m/%Y')}"
    else:
        periodo_str = "Período variável por plataforma"

    st.markdown(
        '<div style="font-weight:800; font-size:26px; color:#3D2B1F; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Visão Geral</div>'
        '<div style="display:flex; gap:24px; align-items:center; margin-bottom:20px;">'
        f'<div style="font-size:13px; color:#8B9A2E; letter-spacing:0.1em;">BRAND INTELLIGENCE — BRASIL</div>'
        f'<div style="font-size:11px; color:#7a5c3a; background:#e8ddc8; padding:4px 12px; border-radius:20px;">Última atualização: {data_coleta_str}</div>'
        f'<div style="font-size:11px; color:#7a5c3a; background:#e8ddc8; padding:4px 12px; border-radius:20px;">Período: {periodo_str}</div>'
        '</div>',
        unsafe_allow_html=True
    )

    total = len(df_f)
    nota_media = df_f["nota"].mean()
    pct_pos = len(df_f[df_f["sentimento"] == "Positivo"]) / total * 100 if total > 0 else 0
    pct_neg = len(df_f[df_f["sentimento"] == "Negativo"]) / total * 100 if total > 0 else 0
    nota_norm = ((nota_media - 1) / 4) * 40 if pd.notna(nota_media) else 0
    sent_norm = pct_pos * 0.6
    indice = min(round(nota_norm + sent_norm), 100)
    if indice >= 70:
        cor_indice = VERDE
        classificacao = "Boa reputação"
    elif indice >= 50:
        cor_indice = "#B8923A"
        classificacao = "Reputação regular"
    else:
        cor_indice = VERMELHO
        classificacao = "Reputação crítica"

    col_ind, col_metrics = st.columns([1, 3])
    with col_ind:
        st.markdown(
            f'<div class="indice-card">'
            f'<div class="indice-valor" style="color:{cor_indice}">{indice}</div>'
            f'<div class="indice-label">Índice de Reputação</div>'
            f'<div class="indice-sub">{classificacao}</div>'
            f'<div style="font-size:10px; color:#b0a090; margin-top:12px; line-height:1.6;">'
            f'* Índice de 0 a 100 calculado com base em:<br>'
            f'40% nota média das avaliações (escala 1–5)<br>'
            f'60% percentual de sentimento positivo<br>'
            f'Fontes: Google Reviews, TripAdvisor, iFood'
            f'</div></div>',
            unsafe_allow_html=True
        )
    with col_metrics:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total de Reviews", f"{total:,}")
        with c2:
            st.metric("Nota Média", f"{nota_media:.1f} / 5" if pd.notna(nota_media) else "—")
        with c3:
            st.metric("% Positivo", f"{pct_pos:.0f}%")
        with c4:
            st.metric("% Negativo", f"{pct_neg:.0f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        with st.container(border=True):
            st.markdown('<div class="section-title">Polaridade Geral</div>', unsafe_allow_html=True)
            contagem = df_f["sentimento"].value_counts().reset_index()
            contagem.columns = ["Sentimento", "Total"]
            fig1 = px.pie(contagem, values="Total", names="Sentimento", color="Sentimento", color_discrete_map=CORES_SENT, hole=0.6)
            fig1.update_traces(textfont_family="Nunito", textfont_size=13)
            fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), legend=dict(font=dict(family="Nunito", size=12, color=MARROM)), font=dict(family="Nunito"))
            st.plotly_chart(fig1, use_container_width=True, key="fig1")

    with col_b:
        with st.container(border=True):
            st.markdown('<div class="section-title">Nota Média por Filial e Plataforma</div>', unsafe_allow_html=True)
            nota_heat = df_f.groupby(["filial", "plataforma"])["nota"].mean().reset_index()
            nota_pivot = nota_heat.pivot(index="filial", columns="plataforma", values="nota").round(1)
            z_values = nota_pivot.values
            text_values = np.where(np.isnan(z_values), "", z_values.round(1).astype(str))
            fig2 = go.Figure(data=go.Heatmap(z=z_values, x=nota_pivot.columns.tolist(), y=nota_pivot.index.tolist(), colorscale=[[0, VERMELHO], [0.4, "#B8923A"], [1, VERDE]], zmin=1, zmax=5, text=text_values, texttemplate="%{text}", textfont=dict(family="Nunito", size=13, color="white"), hoverongaps=False))
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), xaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM), title=""), yaxis=dict(tickfont=dict(family="Nunito", size=11, color=MARROM), title=""), font=dict(family="Nunito"), coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True, key="fig2")

    col_c, col_d = st.columns(2)
    with col_c:
        with st.container(border=True):
            st.markdown('<div class="section-title">Temas Mais Citados</div>', unsafe_allow_html=True)
            temas = df_f["tema"].dropna().str.split(", ").explode()
            temas = temas[~temas.isin(["Sem tema", "Geral"])]
            tema_count = temas.value_counts().reset_index()
            tema_count.columns = ["Tema", "Total"]
            tema_count = tema_count.sort_values("Total", ascending=True)
            fig3 = px.bar(tema_count, x="Total", y="Tema", orientation="h", color="Total", color_continuous_scale=[[0, BEGE], [1, VERDE]], text="Total")
            fig3.update_traces(textposition="outside", textfont=dict(family="Nunito", size=11, color=MARROM))
            fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=40), coloraxis_showscale=False, xaxis=dict(showgrid=False, zeroline=False, title=""), yaxis=dict(title="", tickfont=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"))
            st.plotly_chart(fig3, use_container_width=True, key="fig3")

    with col_d:
        with st.container(border=True):
            st.markdown('<div class="section-title">Sentimento por Plataforma</div>', unsafe_allow_html=True)
            sent_plat = df_f.groupby(["plataforma", "sentimento"]).size().reset_index(name="Total")
            fig4 = px.bar(sent_plat, x="plataforma", y="Total", color="sentimento", color_discrete_map=CORES_SENT, barmode="group", text="Total")
            fig4.update_traces(textposition="outside", textfont=dict(family="Nunito", size=11))
            fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), legend=dict(title="", font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02), xaxis=dict(title="", tickfont=dict(family="Nunito", size=11, color=MARROM)), yaxis=dict(title="", showgrid=False, tickfont=dict(family="Nunito", size=11)), font=dict(family="Nunito"))
            st.plotly_chart(fig4, use_container_width=True, key="fig4")

    col_e, col_f = st.columns(2)
    with col_e:
        with st.container(border=True):
            st.markdown('<div class="section-title">Evolução da Nota Média</div>', unsafe_allow_html=True)
            df_tempo = df_f.copy()
            df_tempo["data_coleta"] = pd.to_datetime(df_tempo["data_coleta"], errors="coerce")
            df_tempo = df_tempo.dropna(subset=["data_coleta"])
            if len(df_tempo) > 0:
                df_tempo["mes"] = df_tempo["data_coleta"].dt.strftime("%b/%Y")
                evolucao = df_tempo.groupby("mes")["nota"].mean().reset_index()
                evolucao.columns = ["Mês", "Nota Média"]
                evolucao["Nota Média"] = evolucao["Nota Média"].round(2)
                fig5 = go.Figure()
                fig5.add_trace(go.Scatter(
                    x=evolucao["Mês"],
                    y=evolucao["Nota Média"],
                    mode="lines+markers+text",
                    fill="tozeroy",
                    fillcolor="rgba(139,154,46,0.15)",
                    line=dict(color=VERDE, width=3),
                    marker=dict(size=8, color=VERDE),
                    text=evolucao["Nota Média"],
                    textposition="top center",
                    textfont=dict(family="Nunito", size=11, color=MARROM),
                ))
                fig5.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, b=10, l=10, r=10),
                    xaxis=dict(title="", tickfont=dict(family="Nunito", size=11, color=MARROM), showgrid=False),
                    yaxis=dict(title="", range=[0, 5.5], showgrid=True, gridcolor="#e8ddc8", tickfont=dict(family="Nunito", size=11)),
                    font=dict(family="Nunito")
                )
                st.plotly_chart(fig5, use_container_width=True, key="fig5")

    with col_f:
        with st.container(border=True):
            st.markdown('<div class="section-title">Palavras Mais Citadas nos Negativos</div>', unsafe_allow_html=True)
            textos_neg = df_f[df_f["sentimento"] == "Negativo"]["texto"].dropna()
            if len(textos_neg) > 0:
                texto_completo = " ".join(textos_neg.tolist())
                texto_completo = re.sub(r'[^\w\s]', ' ', texto_completo.lower())
                palavras = [p for p in texto_completo.split() if p not in STOPWORDS_PT and len(p) > 3]
                freq = pd.Series(palavras).value_counts().head(20).reset_index()
                freq.columns = ["Palavra", "Frequência"]
                fig_tree = px.treemap(freq, path=["Palavra"], values="Frequência", color="Frequência", color_continuous_scale=[[0, "#e8ddc8"], [0.5, "#B8923A"], [1, VERMELHO]])
                fig_tree.update_traces(textfont=dict(family="Nunito", size=14, color="white"), textinfo="label+value")
                fig_tree.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), coloraxis_showscale=False, font=dict(family="Nunito"))
                st.plotly_chart(fig_tree, use_container_width=True, key="fig_tree")

    st.markdown("<br>", unsafe_allow_html=True)
    col_g, col_h = st.columns(2)

    with col_g:
        with st.container(border=True):
            st.markdown('<div class="section-title">Ranking de Filiais</div>', unsafe_allow_html=True)
            ranking = df_f.groupby("filial").agg(
                nota_media=("nota", "mean"),
                total=("nota", "count"),
                pct_pos=("sentimento", lambda x: (x == "Positivo").sum() / len(x) * 100)
            ).reset_index()
            ranking["indice"] = (((ranking["nota_media"] - 1) / 4) * 40 + ranking["pct_pos"] * 0.6).clip(0, 100).round(0).astype(int)
            ranking = ranking.sort_values("indice", ascending=False).reset_index(drop=True)
            html_ranking = ""
            for i, row in ranking.iterrows():
                if row["indice"] >= 70:
                    badge_class, badge_text = "badge-green", "Boa reputação"
                elif row["indice"] >= 50:
                    badge_class, badge_text = "badge-yellow", "Regular"
                else:
                    badge_class, badge_text = "badge-red", "Crítica"
                filial_curta = row["filial"].replace("Olive Garden - ", "")
                html_ranking += (
                    f'<div class="ranking-row">'
                    f'<div class="ranking-pos">#{i+1}</div>'
                    f'<div class="ranking-nome">{filial_curta}</div>'
                    f'<span class="ranking-badge {badge_class}">{badge_text}</span>'
                    f'<div class="ranking-nota">{row["indice"]}</div>'
                    f'</div>'
                )
            st.markdown(html_ranking, unsafe_allow_html=True)

    with col_h:
        with st.container(border=True):
            st.markdown('<div class="section-title">Nota Média por Tema</div>', unsafe_allow_html=True)
            df_temas = df_f.copy()
            df_temas["tema_individual"] = df_temas["tema"].str.split(", ")
            df_temas = df_temas.explode("tema_individual")
            df_temas = df_temas[~df_temas["tema_individual"].isin(["Sem tema", "Geral", None])]
            nota_tema = df_temas.groupby("tema_individual")["nota"].mean().reset_index()
            nota_tema.columns = ["Tema", "Nota"]
            nota_tema = nota_tema.sort_values("Nota", ascending=True)
            fig_tema = px.bar(nota_tema, x="Nota", y="Tema", orientation="h", color="Nota", color_continuous_scale=[[0, VERMELHO], [0.5, "#B8923A"], [1, VERDE]], range_color=[1, 5], text=nota_tema["Nota"].round(1))
            fig_tema.update_traces(textposition="outside", textfont=dict(family="Nunito", size=11, color=MARROM))
            fig_tema.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=50), coloraxis_showscale=False, xaxis=dict(range=[0, 6], showgrid=False, zeroline=False, title=""), yaxis=dict(title="", tickfont=dict(family="Nunito", size=11, color=MARROM)), font=dict(family="Nunito"))
            st.plotly_chart(fig_tema, use_container_width=True, key="fig_tema")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-title">Distribuição de Notas</div>', unsafe_allow_html=True)
        dist_notas = df_f["nota"].dropna().astype(int).value_counts().reset_index()
        dist_notas.columns = ["Nota", "Total"]
        dist_notas = dist_notas.sort_values("Nota")
        dist_notas["Estrelas"] = dist_notas["Nota"].apply(lambda x: "★" * x)
        fig_dist = px.bar(dist_notas, x="Estrelas", y="Total", color="Nota", color_continuous_scale=[[0, VERMELHO], [0.5, "#B8923A"], [1, VERDE]], range_color=[1, 5], text="Total")
        fig_dist.update_traces(textposition="outside", textfont=dict(family="Nunito", size=12, color=MARROM))
        fig_dist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), coloraxis_showscale=False, xaxis=dict(title="", tickfont=dict(family="Nunito", size=14, color=MARROM)), yaxis=dict(title="", showgrid=False, tickfont=dict(family="Nunito", size=11)), font=dict(family="Nunito"))
        st.plotly_chart(fig_dist, use_container_width=True, key="fig_dist")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-title">Reviews Recentes</div>', unsafe_allow_html=True)
        colunas = ["filial", "plataforma", "autor", "nota", "sentimento", "tema", "texto"]
        df_tabela = df_f[colunas].copy()
        df_tabela.columns = ["Filial", "Plataforma", "Autor", "Nota", "Sentimento", "Tema", "Comentário"]
        st.dataframe(df_tabela.head(30), use_container_width=True, hide_index=True)

        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_tabela.sort_values("Nota").to_excel(writer, index=False, sheet_name="Reviews")
        st.download_button(
            label="⬇️ Baixar em Excel",
            data=buffer.getvalue(),
            file_name="reviews_olive_garden.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

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
    df_news_f = df_news_f[df_news_f["publicado_em"] >= data_corte]
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
                    f'<div style="padding:10px 0; border-bottom:1px solid #e8ddc8;">'
                    f'<div style="display:flex; justify-content:space-between; align-items:flex-start;">'
                    f'<a href="{row["url"]}" target="_blank" style="font-size:13px; font-weight:700; color:#3D2B1F; text-decoration:none; flex:1; margin-right:12px;">{row["titulo"]} ↗</a>'
                    f'<span style="font-size:10px; color:#b0a090; white-space:nowrap;">{data}</span>'
                    f'</div>'
                    f'<div style="font-size:12px; color:#7a5c3a; margin-top:4px;">{row["descricao"] or ""}</div>'
                    f'<div style="font-size:10px; color:#8B9A2E; margin-top:4px; font-weight:700;">{row["fonte"]}</div>'
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

    # Análise cruzada 1 — Score Interno vs Reputação Pública
    with st.container(border=True):
        st.markdown('<div class="section-title">Score Interno vs Reputação Pública por Filial</div>', unsafe_allow_html=True)

        # Score interno por filial
        df_comments_f = df_comments[df_comments["filial"].notna() & (df_comments["filial"] != "nan")]
        interno = df_comments_f.groupby("filial").apply(
            lambda x: len(x[x["overall_rating"] == "Highly Satisfied"]) / len(x) * 100
        ).reset_index()
        interno.columns = ["filial", "score_interno"]

        # Score externo por filial
        externo = df.groupby("filial").agg(
            nota_media=("nota", "mean"),
            pct_pos=("sentimento", lambda x: (x == "Positivo").sum() / len(x) * 100)
        ).reset_index()
        externo["score_externo"] = (((externo["nota_media"] - 1) / 4) * 40 + externo["pct_pos"] * 0.6).clip(0, 100).round(1)

        # Cruza os dois
        cruzado = pd.merge(interno, externo[["filial", "score_externo"]], on="filial", how="outer")
        cruzado["filial_curta"] = cruzado["filial"].str.replace("Olive Garden - ", "")
        cruzado["score_interno"] = cruzado["score_interno"].round(1)
        cruzado["divergencia"] = (cruzado["score_interno"] - cruzado["score_externo"]).round(1)

        fig_cross = go.Figure()
        fig_cross.add_trace(go.Bar(
            name="Score Interno (% Highly Satisfied)",
            x=cruzado["filial_curta"],
            y=cruzado["score_interno"],
            marker_color=VERDE,
            text=cruzado["score_interno"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
        ))
        fig_cross.add_trace(go.Bar(
            name="Índice de Reputação Público",
            x=cruzado["filial_curta"],
            y=cruzado["score_externo"],
            marker_color="#B8923A",
            text=cruzado["score_externo"].apply(lambda x: f"{x:.1f}"),
            textposition="outside",
        ))
        fig_cross.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(font=dict(family="Nunito", size=11, color=MARROM), orientation="h", yanchor="bottom", y=1.02),
            xaxis=dict(title="", tickfont=dict(family="Nunito", size=11, color=MARROM)),
            yaxis=dict(title="", range=[0, 115], showgrid=False),
            font=dict(family="Nunito")
        )
        st.plotly_chart(fig_cross, use_container_width=True, key="fig_cross")

        # Tabela de divergências
        st.markdown('<div style="font-size:11px; font-weight:700; color:#8B9A2E; margin-top:8px; margin-bottom:8px;">Divergências detectadas:</div>', unsafe_allow_html=True)
        for _, row in cruzado.sort_values("divergencia").iterrows():
            div = row["divergencia"]
            if pd.isna(div):
                continue
            if div > 10:
                cor = "#2e6b3e"
                icone = "⬆️"
                msg = "Score interno bem acima do público — oportunidade de amplificar reputação"
            elif div < -10:
                cor = "#7a2424"
                icone = "⬇️"
                msg = "Score público abaixo do interno — risco de reputação"
            else:
                cor = "#7a5c1a"
                icone = "≈"
                msg = "Alinhado"
            st.markdown(
                f'<div style="padding:6px 0; border-bottom:1px solid #e8ddc8; display:flex; justify-content:space-between;">'
                f'<span style="font-size:12px; color:{cor}; font-weight:700;">{icone} {row["filial_curta"]}</span>'
                f'<span style="font-size:12px; color:#3D2B1F;">Interno: {row["score_interno"]:.1f}% | Público: {row["score_externo"]:.1f} | Δ {div:+.1f}</span>'
                f'<span style="font-size:11px; color:#b0a090;">{msg}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Análise cruzada 2 — Heatmap de Performance
    with st.container(border=True):
        st.markdown('<div class="section-title">Performance por Dimensão e Filial (% Topbox)</div>', unsafe_allow_html=True)
        if len(df_perf) > 0:
            df_perf_f = df_perf[df_perf["restaurant"] != "nan"].copy()
            df_perf_f["filial_curta"] = df_perf_f["restaurant"].str.replace("Olive Garden - ", "")
            metricas = ["overall_experience", "value", "service", "taste", "speed_of_service", "clean", "soup_salad_refill", "breadstick_refill"]
            labels = ["Experiência Geral", "Valor", "Atendimento", "Sabor", "Velocidade", "Limpeza", "Refil Sopa/Salada", "Refil Breadstick"]
            pivot = df_perf_f.set_index("filial_curta")[metricas]
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

elif aba_sel == "OlivIA":
    import base64 as b64
    with open("assets/Olivia_Fundo_Branco_Header.png", "rb") as img_f:
        olivia_img = b64.b64encode(img_f.read()).decode("utf-8")
    st.markdown(
        f"""<div style="background:#3D2B1F; border-radius:16px; overflow:hidden; display:flex; align-items:stretch; min-height:280px; margin-bottom:24px;">
        <div style="flex:1; padding:52px 40px 52px 56px; display:flex; flex-direction:column; justify-content:center;">
        <div style="font-size:10px; letter-spacing:5px; color:#8B9A2E; text-transform:uppercase; margin-bottom:16px; font-family:Arial,sans-serif;">Agente de inteligencia - Olive Garden Brasil</div>
        <div style="margin-bottom:12px; line-height:1;">
        <span style="font-family:Georgia,serif; font-size:72px; font-weight:800; letter-spacing:2px; color:#F5F0E8;">Oliv<span style="color:#8B9A2E;">ia</span></span>
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
    def preparar_contexto():
        total_reviews = len(df)
        nota_media = df["nota"].mean()
        pct_pos = len(df[df["sentimento"] == "Positivo"]) / len(df) * 100
        pct_neg = len(df[df["sentimento"] == "Negativo"]) / len(df) * 100

        ranking = df.groupby("filial").agg(
            nota_media=("nota", "mean"),
            total=("nota", "count"),
            pct_pos=("sentimento", lambda x: (x == "Positivo").sum() / len(x) * 100)
        ).reset_index()
        ranking["indice"] = (((ranking["nota_media"] - 1) / 4) * 40 + ranking["pct_pos"] * 0.6).clip(0, 100).round(1)
        ranking = ranking.sort_values("indice", ascending=False)

        temas = df["tema"].dropna().str.split(", ").explode()
        temas = temas[~temas.isin(["Sem tema", "Geral"])]
        top_temas = temas.value_counts().head(5).to_dict()

        negativos = df[df["sentimento"] == "Negativo"]["texto"].dropna().head(10).tolist()

        total_social = len(df_social)
        pct_pos_social = len(df_social[df_social["sentimento"] == "Positivo"]) / total_social * 100 if total_social > 0 else 0

        noticias_recentes = df_news[["categoria", "titulo"]].head(10).to_dict("records")

        perf_data = ""
        if len(df_perf) > 0:
            df_perf_ctx = df_perf[df_perf["restaurant"] != "nan"].copy()
            for _, row in df_perf_ctx.iterrows():
                perf_data += f"\n- {row['restaurant']}: Experiência {row['overall_experience']:.1f}% | Sabor {row['taste']:.1f}% | Atendimento {row['service']:.1f}% | Valor {row['value']:.1f}% | Velocidade {row['speed_of_service']:.1f}%"

        pesquisa_data = ""
        if len(df_comments) > 0:
            df_com_ctx = df_comments[df_comments["filial"].notna() & (df_comments["filial"] != "nan")]
            sat_ctx = df_com_ctx.groupby("filial").apply(
                lambda x: len(x[x["overall_rating"] == "Highly Satisfied"]) / len(x) * 100
            ).reset_index()
            sat_ctx.columns = ["filial", "pct_hs"]
            for _, row in sat_ctx.iterrows():
                pesquisa_data += f"\n- {row['filial']}: {row['pct_hs']:.1f}% Highly Satisfied"

        contexto = f"""
Você é um consultor especialista em brand intelligence e gestão de restaurantes. 
Analise os dados abaixo do Olive Garden Brasil e forneça insights estratégicos profissionais.

=== DADOS DE REVIEWS PÚBLICOS ===
Total de reviews: {total_reviews}
Nota média geral: {nota_media:.2f}/5
Sentimento positivo: {pct_pos:.1f}%
Sentimento negativo: {pct_neg:.1f}%

Ranking de filiais por Índice de Reputação:
{ranking[['filial', 'indice', 'nota_media', 'pct_pos']].to_string(index=False)}

Temas mais citados: {top_temas}

Exemplos de comentários negativos recentes:
{chr(10).join([f'- {t[:150]}' for t in negativos[:5]])}

=== DADOS DE REDES SOCIAIS (Instagram) ===
Total de comentários: {total_social}
Sentimento positivo: {pct_pos_social:.1f}%

=== DADOS DE PESQUISA INTERNA (% Highly Satisfied) ===
{pesquisa_data}

=== PERFORMANCE INTERNA (% Topbox) ==={perf_data}

=== NOTÍCIAS RECENTES ===
{chr(10).join([f'[{n["categoria"]}] {n["titulo"]}' for n in noticias_recentes])}
"""
        return contexto

    # Inicializa histórico do chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "analise_gerada" not in st.session_state:
        st.session_state.analise_gerada = False

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    client_ai = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    contexto = preparar_contexto()

    # Botão de análise automática
    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        if st.button("📊 Gerar Briefing Executivo", use_container_width=True, key="btn_briefing"):
            with st.spinner("Analisando todos os dados..."):
                prompt_briefing = """
Analise todos os dados fornecidos e gere um briefing executivo completo sobre a saúde da marca Olive Garden Brasil.

Estruture sua análise nos seguintes blocos, sendo direto, objetivo e acionável:

**1. SAÚDE GERAL DA MARCA**
Avalie o estado atual da reputação com base nos índices, notas e sentimentos. Use os números reais.

**2. DESTAQUES POSITIVOS**
O que está funcionando bem? Quais filiais, dimensões ou plataformas se destacam positivamente?

**3. PONTOS DE ATENÇÃO**
O que requer ação imediata? Seja específico sobre filiais, temas e plataformas com problemas.

**4. DIVERGÊNCIAS INTERNAS vs EXTERNAS**
Onde há diferença significativa entre a percepção interna (pesquisa) e a reputação pública? O que isso indica?

**5. TENDÊNCIAS DE MERCADO RELEVANTES**
Com base nas notícias recentes, quais movimentos do mercado impactam diretamente o Olive Garden Brasil?

**6. TOP 3 RECOMENDAÇÕES PRIORITÁRIAS**
As 3 ações mais importantes que a gestão deve tomar agora, ordenadas por impacto.

Seja direto como um consultor sênior apresentando para o CEO. Use dados reais, evite generalidades e termine cada bloco com uma conclusão clara.
"""
                response = client_ai.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=2500,
                    system=contexto,
                    messages=[{"role": "user", "content": prompt_briefing}]
                )
                st.session_state.chat_history = [{
                    "role": "assistant",
                    "content": response.content[0].text
                }]
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Exibe histórico do chat
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div style="background:#e8ddc8; border-radius:10px; padding:12px 16px; margin-bottom:8px; text-align:right;">'
                f'<div style="font-size:13px; color:#3D2B1F;">{msg["content"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            with st.container(border=True):
                st.markdown(f'<div style="font-size:12px; line-height:1.7; color:#3D2B1F; font-family:Nunito,sans-serif;">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input do chat
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-title">Pergunte ao Agente</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px; color:#b0a090; margin-bottom:12px;">Exemplos: "Qual filial precisa de atenção urgente?" • "O que os clientes mais elogiam?" • "Como melhorar o score do iFood?"</div>', unsafe_allow_html=True)

        pergunta = st.text_input("", placeholder="Digite sua pergunta sobre os dados do Olive Garden Brasil...", key="pergunta_ia", label_visibility="collapsed")

        if st.button("Enviar", key="btn_enviar", use_container_width=False):
            if pergunta:
                st.session_state.chat_history.append({"role": "user", "content": pergunta})
                with st.spinner("Analisando..."):
                    mensagens = []
                    for msg in st.session_state.chat_history:
                        mensagens.append({"role": msg["role"], "content": msg["content"]})
                    response = client_ai.messages.create(
                        model="claude-opus-4-5",
                        max_tokens=1500,
                        system=contexto,
                        messages=mensagens
                    )
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response.content[0].text
                    })
                st.rerun()

        if st.button("🗑️ Limpar conversa", key="btn_limpar"):
            st.session_state.chat_history = []
            st.rerun()

st.markdown(
    '<div style="text-align:center; font-size:10px; color:#B8A898; letter-spacing:0.1em; padding-top:20px;">'
    'OLIVE GARDEN BRAND INTELLIGENCE © 2026</div>',
    unsafe_allow_html=True
)





