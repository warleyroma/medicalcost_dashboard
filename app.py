import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import numpy as np

# ---------------------------
# Configuração inicial
# ---------------------------
st.set_page_config(
    page_title="Insurance Dashboard - Análise Avançada",
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
    
    # Feature Engineering - Criação de variáveis para análises avançadas
    # Faixa Etária
    bins = [0, 30, 45, 60, 100]
    labels = ['18-30', '31-45', '46-60', '60+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    
    # Categoria de IMC
    bins_imc = [0, 18.5, 24.9, 29.9, 100]
    labels_imc = ['Abaixo do peso', 'Normal', 'Sobrepeso', 'Obeso']
    df['bmi_category'] = pd.cut(df['bmi'], bins=bins_imc, labels=labels_imc, right=False)
    
    # Categoria de Risco (baseado em tabagismo e IMC)
    df['risk_category'] = df.apply(
        lambda row: 'Alto Risco' if row['smoker'] == 'yes' and row['bmi'] >= 30 else
                   'Risco Moderado' if row['smoker'] == 'yes' or row['bmi'] >= 30 else
                   'Baixo Risco',
        axis=1
    )
    
    # Score de Risco (simples)
    df['risk_score'] = df.apply(
        lambda row: 3 if row['smoker'] == 'yes' and row['bmi'] >= 30 else
                   2 if row['smoker'] == 'yes' or row['bmi'] >= 30 else
                   1,
        axis=1
    )
    
    return df

df = load_data()

# ---------------------------
# Sidebar - Tema e Filtros
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

# Filtros Interativos
st.sidebar.divider()
st.sidebar.subheader("🔍 Filtros")

# Filtro de Fumante
smoker_filter = st.sidebar.multiselect(
    "Fumante",
    options=df['smoker'].unique(),
    default=df['smoker'].unique()
)

# Filtro de Faixa Etária
age_filter = st.sidebar.multiselect(
    "Faixa Etária",
    options=df['age_group'].unique(),
    default=df['age_group'].unique()
)

# Filtro de Região
region_filter = st.sidebar.multiselect(
    "Região",
    options=df['region'].unique(),
    default=df['region'].unique()
)

# Aplicar filtros
df_filtered = df[
    (df['smoker'].isin(smoker_filter)) &
    (df['age_group'].isin(age_filter)) &
    (df['region'].isin(region_filter))
]

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
    
    /* Custom cards para análise */
    .insight-card {{
        background-color: {CARD_COLOR};
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #3b82f6;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Funções auxiliares
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

def calculate_kpis(df):
    """Calcula KPIs principais"""
    kpis = {
        'total_pessoas': len(df),
        'custo_medio': df['charges'].mean(),
        'custo_mediano': df['charges'].median(),
        'custo_max': df['charges'].max(),
        'custo_fumante': df[df['smoker'] == 'yes']['charges'].mean(),
        'custo_nao_fumante': df[df['smoker'] == 'no']['charges'].mean(),
        'percentual_fumantes': (df['smoker'] == 'yes').mean() * 100,
        'custo_maior_idade': df[df['age'] > 55]['charges'].mean(),
        'custo_menor_idade': df[df['age'] <= 30]['charges'].mean(),
    }
    return kpis

# ---------------------------
# Header
# ---------------------------
st.title("🏥 Insurance Cost Dashboard - Análise Avançada")
st.caption("Análise interativa de custos médicos com insights de negócio")

# Mensagem de carregamento
if "mensagem_exibida" not in st.session_state:
    st.session_state.mensagem_exibida = False

if not st.session_state.mensagem_exibida:
    alerta = st.empty()
    alerta.success("Dados carregados com sucesso 🚀")
    time.sleep(3)
    alerta.empty()
    st.session_state.mensagem_exibida = True

# ---------------------------
# KPIs Avançados (5 colunas)
# ---------------------------
kpis = calculate_kpis(df_filtered)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "👥 Pessoas",
        f"{kpis['total_pessoas']:,}"
    )

with col2:
    st.metric(
        "💰 Custo Médio",
        f"${kpis['custo_medio']:,.2f}"
    )

with col3:
    st.metric(
        "🚬 Custo Fumante",
        f"${kpis['custo_fumante']:,.2f}",
        delta=f"{(kpis['custo_fumante']/kpis['custo_nao_fumante'] - 1)*100:.1f}% maior"
    )

with col4:
    st.metric(
        "✅ Custo Não-Fumante",
        f"${kpis['custo_nao_fumante']:,.2f}"
    )

with col5:
    st.metric(
        "📈 % Fumantes",
        f"{kpis['percentual_fumantes']:.1f}%"
    )

st.divider()

# ---------------------------
# INSIGHTS DE NEGÓCIO (Cards)
# ---------------------------
st.subheader("💡 Insights Estratégicos")

col_insight1, col_insight2, col_insight3 = st.columns(3)

with col_insight1:
    st.markdown(f"""
    <div class="insight-card">
        <h4>🚬 Impacto do Tabagismo</h4>
        <p style="font-size: 24px; font-weight: bold; color: #ef4444;">
            {((kpis['custo_fumante']/kpis['custo_nao_fumante'] - 1)*100):.0f}%
        </p>
        <p>Fumantes custam em média <b>{((kpis['custo_fumante']/kpis['custo_nao_fumante'] - 1)*100):.0f}% mais</b> que não-fumantes</p>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    st.markdown(f"""
    <div class="insight-card" style="border-left-color: #f59e0b;">
        <h4>📈 Efeito da Idade</h4>
        <p style="font-size: 24px; font-weight: bold; color: #f59e0b;">
            {((kpis['custo_maior_idade']/kpis['custo_menor_idade'] - 1)*100):.0f}%
        </p>
        <p>Clientes com 55+ anos custam <b>{((kpis['custo_maior_idade']/kpis['custo_menor_idade'] - 1)*100):.0f}% mais</b> que jovens (≤30 anos)</p>
    </div>
    """, unsafe_allow_html=True)

with col_insight3:
    # Calcular % de alto risco
    pct_alto_risco = (df_filtered[df_filtered['risk_category'] == 'Alto Risco'].shape[0] / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0
    st.markdown(f"""
    <div class="insight-card" style="border-left-color: #8b5cf6;">
        <h4>⚠️ Perfil de Risco</h4>
        <p style="font-size: 24px; font-weight: bold; color: #8b5cf6;">
            {pct_alto_risco:.1f}%
        </p>
        <p>Clientes de <b>Alto Risco</b> (Fumantes + Obesos) representam {pct_alto_risco:.1f}% da base</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------
# GRÁFICOS PRINCIPAIS (2 colunas)
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    # Histograma com médias
    hist = px.histogram(
        df_filtered,
        x="charges",
        nbins=40,
        title="📊 Distribuição dos Custos Médicos",
        labels={"charges": "Custo médico (US$)"},
        color_discrete_sequence=['#3b82f6']
    )

    hist.add_vline(
        x=df_filtered["charges"].median(),
        line_dash="dash",
        line_color="#3b82f6",
        annotation_text=f"Mediana: ${df_filtered['charges'].median():,.0f}",
        annotation_position="top"
    )

    hist.add_vline(
        x=df_filtered["charges"].mean(),
        line_dash="dash",
        line_color="#ef4444",
        annotation_text=f"Média: ${df_filtered['charges'].mean():,.0f}",
        annotation_position="bottom"
    )
    
    apply_plot_theme(hist)
    st.plotly_chart(hist, use_container_width=True)

with col2:
    # Scatter: IMC vs Custo colorido por tabagismo
    scatter = px.scatter(
        df_filtered,
        x="bmi",
        y="charges",
        color="smoker",
        title="📈 Relação IMC vs Custos Médicos",
        labels={
            "bmi": "IMC",
            "charges": "Custo médico (US$)",
            "smoker": "Tabagismo"
        },
        opacity=0.65,
        trendline="ols",
        color_discrete_map={'yes': '#ef4444', 'no': '#3b82f6'}
    )
    apply_plot_theme(scatter)
    st.plotly_chart(scatter, use_container_width=True)

# ---------------------------
# GRÁFICOS DE ANÁLISE AVANÇADA (3 colunas)
# ---------------------------
st.subheader("🔬 Análises Avançadas de Negócio")

col1, col2, col3 = st.columns(3)

with col1:
    # Interação: Idade x Tabagismo
    age_smoker = df_filtered.groupby(['age_group', 'smoker'], as_index=False)['charges'].mean()
    
    bar_age_smoker = px.bar(
        age_smoker,
        x="age_group",
        y="charges",
        color="smoker",
        title="🚬 Custo por Idade e Tabagismo",
        labels={"charges": "Custo Médio (US$)", "age_group": "Faixa Etária"},
        barmode="group",
        color_discrete_map={'yes': '#ef4444', 'no': '#3b82f6'}
    )
    apply_plot_theme(bar_age_smoker)
    st.plotly_chart(bar_age_smoker, use_container_width=True)

with col2:
    # Interação: IMC x Tabagismo
    bmi_smoker = df_filtered.groupby(['bmi_category', 'smoker'], as_index=False)['charges'].mean()
    
    bar_bmi_smoker = px.bar(
        bmi_smoker,
        x="bmi_category",
        y="charges",
        color="smoker",
        title="⚖️ Custo por IMC e Tabagismo",
        labels={"charges": "Custo Médio (US$)", "bmi_category": "Categoria IMC"},
        barmode="group",
        color_discrete_map={'yes': '#ef4444', 'no': '#3b82f6'}
    )
    apply_plot_theme(bar_bmi_smoker)
    st.plotly_chart(bar_bmi_smoker, use_container_width=True)

with col3:
    # Categoria de Risco
    risk_data = df_filtered.groupby('risk_category', as_index=False)['charges'].mean()
    risk_data = risk_data.sort_values('charges', ascending=False)
    
    bar_risk = px.bar(
        risk_data,
        x="risk_category",
        y="charges",
        title="🎯 Custo Médio por Categoria de Risco",
        labels={"charges": "Custo Médio (US$)", "risk_category": "Categoria de Risco"},
        color="risk_category",
        color_discrete_map={
            'Alto Risco': '#ef4444',
            'Risco Moderado': '#f59e0b',
            'Baixo Risco': '#22c55e'
        }
    )
    apply_plot_theme(bar_risk)
    st.plotly_chart(bar_risk, use_container_width=True)

# ---------------------------
# GRÁFICOS SECUNDÁRIOS (3 colunas)
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    # Donut - Fumantes
    donut = px.pie(
        df_filtered,
        names="smoker",
        hole=0.6,
        title="🚬 Distribuição de Fumantes",
        color="smoker",
        color_discrete_map={'yes': '#ef4444', 'no': '#3b82f6'}
    )
    apply_plot_theme(donut)
    st.plotly_chart(donut, use_container_width=True)

with col2:
    # Boxplot - Custo por Região
    box_region = px.box(
        df_filtered,
        x="region",
        y="charges",
        title="📍 Custos por Região",
        labels={"charges": "Custo (US$)", "region": "Região"},
        color="region"
    )
    apply_plot_theme(box_region)
    st.plotly_chart(box_region, use_container_width=True)

with col3:
    # Boxplot - Custo por Número de Filhos
    box_children = px.box(
        df_filtered,
        x="children",
        y="charges",
        title="👨‍👩‍👧‍👦 Custos por Número de Filhos",
        labels={"charges": "Custo (US$)", "children": "Número de Filhos"}
    )
    apply_plot_theme(box_children)
    st.plotly_chart(box_children, use_container_width=True)

# ---------------------------
# ANÁLISE DE CORRELAÇÃO
# ---------------------------
st.subheader("📊 Matriz de Correlação")

# Selecionar colunas numéricas
numeric_cols = ['age', 'bmi', 'children', 'charges']
corr_df = df_filtered[numeric_cols].copy()
corr_df['smoker_encoded'] = (df_filtered['smoker'] == 'yes').astype(int)

# Calcular correlação
corr_matrix = corr_df.corr()

# Criar heatmap
fig_corr = px.imshow(
    corr_matrix,
    text_auto=True,
    title="Matriz de Correlação entre Variáveis",
    labels=dict(color="Correlação"),
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1
)
apply_plot_theme(fig_corr)
st.plotly_chart(fig_corr, use_container_width=True)

# ---------------------------
# TABELA DE DADOS FILTRADA
# ---------------------------
st.subheader("📋 Dados Filtrados")

# Opção para mostrar a tabela
if st.checkbox("Mostrar tabela de dados"):
    st.dataframe(
        df_filtered,
        use_container_width=True,
        height=400
    )

# ---------------------------
# RODAPÉ
# ---------------------------
st.markdown("---")
st.caption("📌 Dashboard de Análise de Seguros • Desenvolvido com Streamlit + Plotly")
