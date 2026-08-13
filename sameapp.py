import pandas as pd
import streamlit as st
import plotly.express as px
import time

# ---------------------------
# Configuração inicial
# ---------------------------
st.set_page_config(
    page_title="Insurance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------
# Carregamento dos dados
# ---------------------------

@st.cache_data
def load_data():
    DATA_PATH = "data/insurance.csv"
    df = pd.read_csv(DATA_PATH)
    return df

df = load_data()

# ---------------------------
# Sidebar - Tema
# ---------------------------
st.sidebar.title("⚙️ Configurações")

theme = st.sidebar.radio(
    "Tema",
    ["🌙 Dark", "☀️ Light"],
    horizontal=True
)

if theme == "🌙 Dark":
    BG_COLOR = "#0f172a"
    CARD_COLOR = "#111827"
    TEXT_COLOR = "#e5e7eb"
    BORDER_COLOR = "#1f2937"
    PLOT_BG = "#0f172a"
else:
    BG_COLOR = "#f8fafc"
    CARD_COLOR = "#ffffff"
    TEXT_COLOR = "#0f172a"
    BORDER_COLOR = "#e5e7eb"
    PLOT_BG = "#ffffff"

# ---------------------------
# CSS GLOBAL
# ---------------------------
st.markdown(f"""
<style>
    .stApp {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
    }}

    h1, h2, h3, h4, h5, h6, p, span, label {{
        color: {TEXT_COLOR} !important;
    }}

    div[data-testid="metric-container"] {{
        background-color: {CARD_COLOR};
        border-radius: 16px;
        padding: 18px;
        border: 1px solid {BORDER_COLOR};
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }}

    section[data-testid="stSidebar"] {{
        background-color: {CARD_COLOR};
        border-right: 1px solid {BORDER_COLOR};
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Função padrão para gráficos
# ---------------------------
def apply_plot_theme(fig):
    fig.update_layout(
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT_COLOR),
        title_font=dict(size=18),
        legend=dict(
            bgcolor=PLOT_BG,
            bordercolor=BORDER_COLOR
        )
    )
    return fig

# ---------------------------
# Header
# ---------------------------
st.title("📊 Insurance Cost Dashboard")
st.caption("Análise interativa de custos médicos baseada em dados reais")

# 1. Inicializa uma variável na memória para controlar se já mostrou a mensagem
if "mensagem_exibida" not in st.session_state:
    st.session_state.mensagem_exibida = False

# 2. Se ainda não mostrou, exibe por 5 segundos e depois apaga
if not st.session_state.mensagem_exibida:
    alerta = st.empty()
    alerta.success("Dados carregados com sucesso 🚀")
    time.sleep(5)
    alerta.empty()
    
    # Marca como exibida para não repetir se a página recarregar
    st.session_state.mensagem_exibida = True

# ---------------------------
# KPIs
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Pessoas analisadas",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "💰 Custo médio",
        f"${df['charges'].mean():,.2f}"
    )

with col3:
    st.metric(
        "📊 Custo mediano",
        f"${df['charges'].median():,.2f}"
    )

with col4:
    st.metric(
        "📈 Custo máximo",
        f"${df['charges'].max():,.2f}"
    )
st.divider()



# ---------------------------
# Gráficos principais
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    hist = px.histogram(
        df,
        x="charges",
        nbins=40,
        title="Distribuição dos custos médicos",
        labels={
            "charges": "Custo médico (US$)"
        }
    )

    hist.add_vline(
        x=df["charges"].median(),
        line_dash="dash",
        line_color="#3b82f6",
        annotation_text="Mediana",
        annotation_position="top"
    )

    hist.add_vline(
        x=df["charges"].mean(),
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="Média",
        annotation_position="top"
    )

    apply_plot_theme(hist)
    st.plotly_chart(hist, use_container_width=True)

with col2:
    scatter = px.scatter(
        df,
        x="bmi",
        y="charges",
        color="smoker",
        title="Relação entre IMC e Custos Médicos",
        labels={
            "bmi": "IMC",
            "charges": "Custo médico (US$)",
            "smoker": "Tabagismo"
        },
        opacity=0.65,
        trendline="ols"
    )
    apply_plot_theme(scatter)
    st.plotly_chart(scatter, use_container_width=True)

# ---------------------------
# Gráficos secundários
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    donut = px.pie(
        df,
        names="smoker",
        hole=0.6,
        title="Distribuição de Fumantes"
    )
    apply_plot_theme(donut)
    st.plotly_chart(donut, use_container_width=True)

with col2:
    bar = px.bar(
        df.groupby("region", as_index=False)["charges"].mean(),
        x="region",
        y="charges",
        title="Custo médio por região"
    )
    apply_plot_theme(bar)
    st.plotly_chart(bar, use_container_width=True)

with col3:
    box = px.box(
        df,
        x="children",
        y="charges",
        title="Custos por número de filhos"
    )
    apply_plot_theme(box)
    st.plotly_chart(box, use_container_width=True)

# ---------------------------
# Rodapé
# ---------------------------
st.markdown("---")
st.caption("📌 Projeto educacional • Streamlit + Plotly • Deploy pronto para Render")
