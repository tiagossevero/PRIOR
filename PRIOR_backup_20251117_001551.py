# ============================================================
# COLE ESTE CÓDIGO NO INÍCIO DE CADA ARQUIVO .PY
# ============================================================
import streamlit as st
import hashlib

# DEFINA A SENHA AQUI
SENHA = "tsevero741"  # ← TROQUE para cada projeto

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("<div style='text-align: center; padding: 50px;'><h1>🔐 Acesso Restrito</h1></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            senha_input = st.text_input("Digite a senha:", type="password", key="pwd_input")
            if st.button("Entrar", use_container_width=True):
                if senha_input == SENHA:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Senha incorreta")
        st.stop()

check_password()


"""
Sistema GECOB - Priorização de Cobrança v1.4
Receita Estadual de Santa Catarina
Dashboard interativo para gestão e priorização de cobranças tributárias
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine
import warnings
import ssl
from datetime import datetime

# =============================================================================
# 1. CONFIGURAÇÕES INICIAIS
# =============================================================================

# Hack SSL
try:
    createunverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = createunverified_https_context

warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="GECOB - Priorização de Cobrança",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1565C0;
        text-align: center;
        padding: 1rem 0;
    }

        /* ESTILO DOS KPIs - BORDA PRETA */
    div[data-testid="stMetric"] {
        background-color: #ffffff;        /* Fundo branco */
        border: 2px solid #2c3e50;        /* Borda: 2px de largura, sólida, cor cinza-escuro */
        border-radius: 10px;              /* Cantos arredondados (10 pixels de raio) */
        padding: 15px;                    /* Espaçamento interno (15px em todos os lados) */
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* Sombra: horizontal=0, vertical=2px, blur=4px, cor preta 10% opacidade */
    }
    
    /* Título do métrica */
    div[data-testid="stMetric"] > label {
        font-weight: 600;                 /* Negrito médio */
        color: #2c3e50;                   /* Cor do texto */
    }
    
    /* Valor do métrica */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;                /* Tamanho da fonte do valor */
        font-weight: bold;                /* Negrito */
        color: #1f77b4;                   /* Cor azul */
    }
    
    /* Delta (variação) */
    div[data-testid="stMetricDelta"] {
        font-size: 0.9rem;                /* Tamanho menor para delta */
        
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
    }
    .priority-max { background-color: #ffebee; border-left: 5px solid #c62828; padding: 1rem; }
    .priority-high { background-color: #fff3e0; border-left: 5px solid #ef6c00; padding: 1rem; }
    .priority-medium { background-color: #fffde7; border-left: 5px solid #f9a825; padding: 1rem; }
    .priority-low { background-color: #e8f5e9; border-left: 5px solid #2e7d32; padding: 1rem; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. CREDENCIAIS E CONEXÃO
# =============================================================================

IMPALA_HOST = 'bdaworkernode02.sef.sc.gov.br'
IMPALA_PORT = 21050
DATABASE = 'gecob'

try:
    IMPALA_USER = st.secrets["impala_credentials"]["user"]
    IMPALA_PASSWORD = st.secrets["impala_credentials"]["password"]
except:
    st.error("⚠️ Credenciais não configuradas. Configure secrets.toml")
    st.stop()

# =============================================================================
# 3. FUNÇÕES DE CARREGAMENTO
# =============================================================================

@st.cache_data(show_spinner="Carregando dados...", ttl=3600)
def carregar_dados_gecob():
    """Carrega dados do sistema GECOB - versão otimizada para Impala"""
    dados = {}
    logs = []
    
    try:
        engine = create_engine(
            f'impala://{IMPALA_HOST}:{IMPALA_PORT}/{DATABASE}',
            connect_args={
                'user': IMPALA_USER,
                'password': IMPALA_PASSWORD,
                'auth_mechanism': 'LDAP',
                'use_ssl': True
            }
        )
        
        logs.append("✅ Conexão estabelecida")
        
        # Configuração de tabelas - carregar tudo de uma vez
        # Impala não suporta OFFSET sem ORDER BY, então carregamos direto
        tabelas_config = {
            'master': {
                'table': 'prior_master_consolidado',
                'colunas_essenciais': [
                    'inscricao_estadual', 'tipo_debito', 'razao_social', 
                    'nome_municipio', 'porte_por_faturamento', 'valor_total_devido',
                    'secao_cnae', 'cnae_classe', 'situacao_cadastral_desc',
                    'qtd_total_contatos', 'flag_falencia', 'flag_recuperacao_judicial',
                    'flag_devedor_contumaz', 'data_inclusao_cobranca',
                    'saldo_imposto', 'saldo_multa', 'saldo_juros'
                ]
            },
            'score': {
                'table': 'prior_score_priorizacao',
                'colunas_essenciais': [
                    'inscricao_estadual', 'tipo_debito', 'valor_total_devido',
                    'score_final_priorizacao', 'classificacao_prioridade',
                    'score_valor_debito', 'score_capacidade_pagamento',
                    'score_historico_pagamento', 'score_responsividade',
                    'score_viabilidade_cobranca', 'score_urgencia', 'score_conformidade'
                ]
            },
            'componentes': {
                'table': 'prior_score_componentes',
                'colunas_essenciais': None  # Carregar todas
            },
            'clusters': {
                'table': 'prior_clusters_empresas',
                'colunas_essenciais': None
            },
            'outliers': {
                'table': 'prior_outliers_identificados',
                'colunas_essenciais': None
            }
        }
        
        for key, config in tabelas_config.items():
            try:
                table_name = config['table']
                colunas = config.get('colunas_essenciais')
                
                # Primeiro, contar registros
                count_query = f"SELECT COUNT(*) as total FROM {DATABASE}.{table_name}"
                total_count = pd.read_sql(count_query, engine).iloc[0]['total']
                
                logs.append(f"📊 {table_name}: {total_count:,} registros")
                
                # Construir query com colunas específicas ou todas
                if colunas:
                    colunas_str = ', '.join(colunas)
                    query = f"SELECT {colunas_str} FROM {DATABASE}.{table_name}"
                else:
                    query = f"SELECT * FROM {DATABASE}.{table_name}"
                
                # Carregar dados
                df = pd.read_sql(query, engine)
                
                # Processar colunas
                df.columns = [col.lower() for col in df.columns]
                
                # Converter tipos de dados
                for col in df.select_dtypes(include=['object']).columns:
                    try:
                        df[col] = pd.to_numeric(df[col], errors='ignore')
                    except:
                        pass
                
                dados[key] = df
                logs.append(f"   ✅ {len(df):,} registros carregados")
                
            except Exception as e:
                erro_msg = f"❌ Erro em {config['table']}: {str(e)[:100]}"
                logs.append(erro_msg)
                dados[key] = pd.DataFrame()
        
        engine.dispose()
        logs.append("🎉 Carregamento completo!")
        
    except Exception as e:
        erro_msg = f"❌ Erro de conexão: {str(e)[:100]}"
        logs.append(erro_msg)
        return {}, logs
    
    # Salvar logs no session_state
    st.session_state['logs_carregamento'] = logs
    st.session_state['conexao_status'] = "✅ Conectado"
    
    return dados

# =============================================================================
# 4. FUNÇÕES AUXILIARES
# =============================================================================

def formatar_moeda(valor):
    if pd.isna(valor): return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor):
    if pd.isna(valor): return "0,00%"
    return f"{valor*100:.2f}%".replace(".", ",")

def criar_grafico_score(df_componentes, inscricao):
    """Cria gráfico radar dos componentes do score"""
    emp = df_componentes[df_componentes['inscricao_estadual'] == inscricao]
    if emp.empty:
        return None
    
    emp = emp.iloc[0]
    categorias = ['Valor', 'Capacidade', 'Histórico', 'Responsividade', 
                  'Viabilidade', 'Urgência', 'Conformidade']
    valores = [
        emp.get('score_valor_debito', 0),
        emp.get('score_capacidade_pagamento', 0),
        emp.get('score_historico_pagamento', 0),
        emp.get('score_responsividade', 0),
        emp.get('score_viabilidade_cobranca', 0),
        emp.get('score_urgencia', 0),
        emp.get('score_conformidade', 0)
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        line_color='#1565C0'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400
    )
    
    return fig

# =============================================================================
# 5. INTERFACE PRINCIPAL
# =============================================================================

def main():
    # Header
    st.markdown('<p class="main-header">💰 GECOB - Sistema de Priorização de Cobrança</p>', 
                unsafe_allow_html=True)
    st.markdown("**Receita Estadual de Santa Catarina** | Versão 1.4")
    st.markdown("---")
    
    # Carregar dados
    with st.spinner("Carregando dados do sistema..."):
        dados = carregar_dados_gecob()
    
    if not dados or all(df.empty for df in dados.values()):
        st.error("❌ Não foi possível carregar os dados")
        return
    
    # Sidebar
    st.sidebar.title("🔐 Navegação")
    secao = st.sidebar.radio(
        "Escolha a análise:",
        [
            "📊 Visão Geral",
            "🎯 Top Prioridades",
            "🔍 Consulta Empresa",
            "📈 Análise Setorial",
            "🗺️ Análise Geográfica",
            "👥 Análise de Clusters",
            "⚠️ Outliers e Casos Críticos",
            "📉 Análise Temporal",
            "🤖 Machine Learning",
            "📋 Relatórios"
        ]
    )
    
    # Status de conexão e logs
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📡 Status do Sistema")
    
    if 'conexao_status' in st.session_state:
        st.sidebar.info(st.session_state['conexao_status'])
    
    # Logs em expander
    if 'logs_carregamento' in st.session_state:
        with st.sidebar.expander("📋 Logs de Carregamento"):
            for log in st.session_state['logs_carregamento']:
                st.sidebar.text(log)
    
    # Renderizar seção
    if secao == "📊 Visão Geral":
        render_visao_geral(dados)
    elif secao == "🎯 Top Prioridades":
        render_top_prioridades(dados)
    elif secao == "🔍 Consulta Empresa":
        render_consulta_empresa(dados)
    elif secao == "📈 Análise Setorial":
        render_analise_setorial(dados)
    elif secao == "🗺️ Análise Geográfica":
        render_analise_geografica(dados)
    elif secao == "👥 Análise de Clusters":
        render_analise_clusters(dados)
    elif secao == "⚠️ Outliers e Casos Críticos":
        render_outliers(dados)
    elif secao == "📉 Análise Temporal":
        render_analise_temporal(dados)
    elif secao == "🤖 Machine Learning":
        render_machine_learning(dados)
    elif secao == "📋 Relatórios":
        render_relatorios(dados)

# =============================================================================
# 6. VISÃO GERAL
# =============================================================================

def render_visao_geral(dados):
    st.header("📊 Visão Geral do Sistema")
    
    df_score = dados.get('score', pd.DataFrame())
    df_master = dados.get('master', pd.DataFrame())
    
    if df_score.empty or df_master.empty:
        st.warning("Dados insuficientes")
        return
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_empresas = df_master['inscricao_estadual'].nunique()
        st.metric("🏢 Empresas", f"{total_empresas:,}")
    
    with col2:
        total_debitos = len(df_master)
        st.metric("📋 Débitos", f"{total_debitos:,}")
    
    with col3:
        valor_total = df_master['valor_total_devido'].sum() / 1e9
        st.metric("💰 Valor Total", f"R$ {valor_total:.2f}B")
    
    with col4:
        score_medio = df_score['score_final_priorizacao'].mean()
        st.metric("📊 Score Médio", f"{score_medio:.1f}")
    
    # Distribuição por prioridade
    st.markdown("---")
    st.subheader("📈 Distribuição por Nível de Prioridade")
    
    prior_dist = df_score['classificacao_prioridade'].value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        cores = {
            'PRIORIDADE_MAXIMA': '#d32f2f',
            'PRIORIDADE_ALTA': '#f57c00',
            'PRIORIDADE_MEDIA': '#fbc02d',
            'PRIORIDADE_BAIXA': '#388e3c'
        }
        
        fig = px.pie(
            values=prior_dist.values,
            names=prior_dist.index,
            title="Distribuição de Débitos",
            color=prior_dist.index,
            color_discrete_map=cores
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Resumo")
        for idx, (prior, qtd) in enumerate(prior_dist.items()):
            pct = (qtd / len(df_score)) * 100
            st.metric(prior.replace('_', ' '), f"{qtd:,}", f"{pct:.1f}%")
    
    # Top 10 maiores débitos
    st.markdown("---")
    st.subheader("🏆 Top 10 Maiores Débitos")
    
    df_top = df_score.nlargest(10, 'valor_total_devido').merge(
        df_master[['inscricao_estadual', 'tipo_debito', 'razao_social']], 
        on=['inscricao_estadual', 'tipo_debito'], 
        how='left'
    )
    
    st.dataframe(
        df_top[['inscricao_estadual', 'razao_social', 'valor_total_devido', 
                'score_final_priorizacao', 'classificacao_prioridade']],
        hide_index=True,
        column_config={
            'inscricao_estadual': 'IE',
            'razao_social': 'Razão Social',
            'valor_total_devido': st.column_config.NumberColumn(
                'Valor Devido',
                format="R$ %.2f"
            ),
            'score_final_priorizacao': st.column_config.NumberColumn(
                'Score',
                format="%.1f"
            ),
            'classificacao_prioridade': 'Prioridade'
        }
    )

# =============================================================================
# 7. TOP PRIORIDADES
# =============================================================================

def render_top_prioridades(dados):
    st.header("🎯 Top Prioridades para Ação")
    
    df_score = dados.get('score', pd.DataFrame())
    df_master = dados.get('master', pd.DataFrame())
    
    if df_score.empty:
        st.warning("Dados não disponíveis")
        return
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        prioridades = ['Todas'] + df_score['classificacao_prioridade'].unique().tolist()
        prior_filtro = st.selectbox("Filtrar por prioridade:", prioridades)
    
    with col2:
        top_n = st.slider("Quantidade de registros:", 10, 100, 50)
    
    # Aplicar filtros
    df_filtrado = df_score.copy()
    if prior_filtro != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['classificacao_prioridade'] == prior_filtro]
    
    df_top = df_filtrado.nlargest(top_n, 'score_final_priorizacao')
    
    # Merge com master
    df_top = df_top.merge(
        df_master[['inscricao_estadual', 'tipo_debito', 'razao_social', 
                   'nome_municipio', 'porte_por_faturamento']], 
        on=['inscricao_estadual', 'tipo_debito'], 
        how='left'
    )
    
    # Exibir
    st.info(f"📊 Mostrando {len(df_top):,} registros")
    
    st.dataframe(
        df_top[[
            'inscricao_estadual', 'razao_social', 'nome_municipio',
            'porte_por_faturamento', 'valor_total_devido',
            'score_final_priorizacao', 'classificacao_prioridade'
        ]],
        hide_index=True,
        column_config={
            'inscricao_estadual': 'IE',
            'razao_social': 'Razão Social',
            'nome_municipio': 'Município',
            'porte_por_faturamento': 'Porte',
            'valor_total_devido': st.column_config.NumberColumn(
                'Valor Devido',
                format="R$ %.2f"
            ),
            'score_final_priorizacao': st.column_config.NumberColumn(
                'Score',
                format="%.1f"
            ),
            'classificacao_prioridade': 'Prioridade'
        },
        height=600
    )
    
    # Download
    csv = df_top.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        "📥 Download CSV",
        csv,
        f"prioridades_{datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )

# =============================================================================
# 8. CONSULTA EMPRESA
# =============================================================================

def render_consulta_empresa(dados):
    st.header("🔍 Consulta Detalhada de Empresa")
    
    df_score = dados.get('score', pd.DataFrame())
    df_master = dados.get('master', pd.DataFrame())
    df_comp = dados.get('componentes', pd.DataFrame())
    
    # Busca
    ie_busca = st.text_input("Digite a Inscrição Estadual:", max_chars=20)
    
    if ie_busca:
        ie_limpo = ie_busca.strip()
        
        # Buscar em ambas as tabelas com diferentes formatos
        emp_score = df_score[
            (df_score['inscricao_estadual'].astype(str) == ie_limpo) |
            (df_score['inscricao_estadual'].astype(str).str.replace(r'\D', '', regex=True) == ie_limpo.replace('.', '').replace('-', '').replace('/', ''))
        ]
        
        emp_master = df_master[
            (df_master['inscricao_estadual'].astype(str) == ie_limpo) |
            (df_master['inscricao_estadual'].astype(str).str.replace(r'\D', '', regex=True) == ie_limpo.replace('.', '').replace('-', '').replace('/', ''))
        ]
        
        if emp_score.empty:
            st.warning(f"❌ IE {ie_limpo} não encontrada")
            st.info(f"💡 Total de IEs no sistema: {df_score['inscricao_estadual'].nunique():,}")
            
            # Mostrar algumas IEs como exemplo
            st.markdown("**Exemplos de IEs cadastradas:**")
            sample_ies = df_score['inscricao_estadual'].head(10).tolist()
            for ie in sample_ies:
                st.text(f"  • {ie}")
            return
        
        emp = emp_score.iloc[0]
        master = emp_master.iloc[0] if not emp_master.empty else None
        
        st.success(f"✅ Empresa encontrada")
        
        # Informações principais
        if master is not None:
            st.markdown(f"### {master.get('razao_social', 'N/A')}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"**Município:** {master.get('nome_municipio', 'N/A')}")
                st.info(f"**Porte:** {master.get('porte_por_faturamento', 'N/A')}")
            
            with col2:
                st.info(f"**CNAE:** {master.get('cnae_classe', 'N/A')}")
                st.info(f"**Setor:** {master.get('secao_cnae', 'N/A')}")
            
            with col3:
                st.info(f"**Situação:** {master.get('situacao_cadastral_desc', 'N/A')}")
        
        # Métricas
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Valor Devido", formatar_moeda(emp['valor_total_devido']))
        
        with col2:
            st.metric("📊 Score", f"{emp['score_final_priorizacao']:.1f}")
        
        with col3:
            prior = emp['classificacao_prioridade']
            cor_map = {
                'PRIORIDADE_MAXIMA': '🔴',
                'PRIORIDADE_ALTA': '🟠',
                'PRIORIDADE_MEDIA': '🟡',
                'PRIORIDADE_BAIXA': '🟢'
            }
            st.metric(f"{cor_map.get(prior, '⚪')} Prioridade", prior.replace('_', ' '))
        
        with col4:
            if master is not None:
                qtd_contatos = master.get('qtd_total_contatos', 0)
                st.metric("📞 Contatos", f"{qtd_contatos:.0f}")
        
        # Gráfico de componentes
        st.markdown("---")
        st.subheader("📊 Análise dos Componentes do Score")
        
        fig = criar_grafico_score(df_comp, ie_limpo)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de componentes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Scores Individuais:**")
            componentes_data = {
                'Componente': [
                    'Valor do Débito',
                    'Capacidade Pagamento',
                    'Histórico Pagamento',
                    'Responsividade'
                ],
                'Score': [
                    emp.get('score_valor_debito', 0),
                    emp.get('score_capacidade_pagamento', 0),
                    emp.get('score_historico_pagamento', 0),
                    emp.get('score_responsividade', 0)
                ]
            }
            st.dataframe(pd.DataFrame(componentes_data), hide_index=True)
        
        with col2:
            st.markdown("**Scores Complementares:**")
            comp_data = {
                'Componente': [
                    'Viabilidade Cobrança',
                    'Urgência',
                    'Conformidade',
                    '**SCORE FINAL**'
                ],
                'Score': [
                    emp.get('score_viabilidade_cobranca', 0),
                    emp.get('score_urgencia', 0),
                    emp.get('score_conformidade', 0),
                    emp['score_final_priorizacao']
                ]
            }
            st.dataframe(pd.DataFrame(comp_data), hide_index=True)

# =============================================================================
# 9. ANÁLISE SETORIAL
# =============================================================================

def render_analise_setorial(dados):
    st.header("📈 Análise Setorial")
    
    df_master = dados.get('master', pd.DataFrame())
    df_score = dados.get('score', pd.DataFrame())
    
    if df_master.empty or df_score.empty:
        st.warning("Dados não disponíveis")
        return
    
    # Merge - usar sufixos para evitar conflitos
    df = df_master.merge(
        df_score[['inscricao_estadual', 'tipo_debito', 'valor_total_devido', 'score_final_priorizacao']], 
        on=['inscricao_estadual', 'tipo_debito'], 
        how='inner',
        suffixes=('_master', '_score')
    )
    
    # Usar coluna de valor do score
    valor_col = 'valor_total_devido' if 'valor_total_devido' in df.columns else 'valor_total_devido_score'
    
    # Análise por seção CNAE
    setor_stats = df.groupby('secao_cnae').agg({
        'inscricao_estadual': 'nunique',
        valor_col: 'sum',
        'score_final_priorizacao': 'mean'
    }).reset_index()
    
    setor_stats.columns = ['setor', 'empresas', 'valor_total', 'score_medio']
    setor_stats = setor_stats.sort_values('valor_total', ascending=False)
    
    # Visualização
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            setor_stats.head(10),
            x='setor',
            y='valor_total',
            title="Top 10 Setores por Valor",
            labels={'setor': 'Setor CNAE', 'valor_total': 'Valor (R$)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            setor_stats,
            x='empresas',
            y='score_medio',
            size='valor_total',
            hover_data=['setor'],
            title="Empresas vs Score Médio por Setor"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela
    st.markdown("---")
    st.subheader("📊 Dados Detalhados por Setor")
    
    st.dataframe(
        setor_stats,
        hide_index=True,
        column_config={
            'setor': 'Setor',
            'empresas': 'Empresas',
            'valor_total': st.column_config.NumberColumn(
                'Valor Total',
                format="R$ %.2f"
            ),
            'score_medio': st.column_config.NumberColumn(
                'Score Médio',
                format="%.1f"
            )
        }
    )

# =============================================================================
# 10. ANÁLISE GEOGRÁFICA
# =============================================================================

def render_analise_geografica(dados):
    st.header("🗺️ Análise Geográfica")
    
    df_master = dados.get('master', pd.DataFrame())
    df_score = dados.get('score', pd.DataFrame())
    
    if df_master.empty or df_score.empty:
        st.warning("Dados não disponíveis")
        return
    
    # Merge apenas com colunas que existem
    merge_cols = ['inscricao_estadual', 'tipo_debito']
    score_cols = merge_cols + ['valor_total_devido', 'score_final_priorizacao']
    
    # Verificar se as colunas existem antes do merge
    available_score_cols = [col for col in score_cols if col in df_score.columns]
    
    df = df_master.merge(
        df_score[available_score_cols], 
        on=merge_cols, 
        how='inner'
    )
    
    # Usar a coluna de valor que estiver disponível
    if 'valor_total_devido_x' in df.columns:
        valor_col = 'valor_total_devido_x'
    elif 'valor_total_devido_y' in df.columns:
        valor_col = 'valor_total_devido_y'
    elif 'valor_total_devido' in df.columns:
        valor_col = 'valor_total_devido'
    else:
        st.error("Coluna de valor não encontrada após merge")
        st.write("Colunas disponíveis:", df.columns.tolist())
        return
    
    # Análise por município
    mun_stats = df.groupby('nome_municipio').agg({
        'inscricao_estadual': 'nunique',
        valor_col: 'sum',
        'score_final_priorizacao': 'mean'
    }).reset_index()
    
    mun_stats.columns = ['municipio', 'empresas', 'valor_total', 'score_medio']
    mun_stats = mun_stats.sort_values('valor_total', ascending=False)
    
    # Top 15 municípios
    st.subheader("🏆 Top 15 Municípios")
    
    top15 = mun_stats.head(15)
    
    fig = px.bar(
        top15,
        x='municipio',
        y='valor_total',
        title="Valor em Cobrança por Município",
        labels={'municipio': 'Município', 'valor_total': 'Valor (R$)'}
    )
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela completa
    st.markdown("---")
    st.dataframe(
        mun_stats,
        hide_index=True,
        column_config={
            'municipio': 'Município',
            'empresas': 'Empresas',
            'valor_total': st.column_config.NumberColumn(
                'Valor Total',
                format="R$ %.2f"
            ),
            'score_medio': st.column_config.NumberColumn(
                'Score Médio',
                format="%.1f"
            )
        },
        height=400
    )

# =============================================================================
# 11. ANÁLISE DE CLUSTERS
# =============================================================================

def render_analise_clusters(dados):
    st.header("👥 Análise de Clusters")
    
    df_clusters = dados.get('clusters', pd.DataFrame())
    
    if df_clusters.empty:
        st.warning("Dados de clusters não disponíveis")
        return
    
    # Estatísticas por cluster
    cluster_stats = df_clusters.groupby('cluster').agg({
        'inscricao_estadual': 'nunique',
        'valor_total': 'sum',
        'dias_cobranca': 'mean',
        'score_priorizacao': 'mean'
    }).reset_index()
    
    cluster_stats.columns = ['cluster', 'empresas', 'valor_total', 'dias_medio', 'score_medio']
    
    # Visualizações
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            cluster_stats,
            values='empresas',
            names='cluster',
            title="Distribuição de Empresas por Cluster"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            cluster_stats,
            x='cluster',
            y='score_medio',
            title="Score Médio por Cluster"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela
    st.markdown("---")
    st.dataframe(
        cluster_stats,
        hide_index=True,
        column_config={
            'cluster': 'Cluster',
            'empresas': 'Empresas',
            'valor_total': st.column_config.NumberColumn(
                'Valor Total',
                format="R$ %.2f"
            ),
            'dias_medio': st.column_config.NumberColumn(
                'Dias Médio',
                format="%.0f"
            ),
            'score_medio': st.column_config.NumberColumn(
                'Score Médio',
                format="%.1f"
            )
        }
    )

# =============================================================================
# 12. OUTLIERS
# =============================================================================

def render_outliers(dados):
    st.header("⚠️ Outliers e Casos Críticos")
    
    df_outliers = dados.get('outliers', pd.DataFrame())
    
    if df_outliers.empty:
        st.warning("Dados de outliers não disponíveis")
        return
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔴 Total Outliers", f"{len(df_outliers):,}")
    
    with col2:
        valor_total = df_outliers['valor_devido'].sum() / 1e9
        st.metric("💰 Valor Total", f"R$ {valor_total:.2f}B")
    
    with col3:
        score_medio = df_outliers['score'].mean()
        st.metric("📊 Score Médio", f"{score_medio:.1f}")
    
    # Top outliers
    st.markdown("---")
    st.subheader("🎯 Top 30 Outliers Mais Críticos")
    
    df_top = df_outliers.nlargest(30, 'valor_devido')
    
    st.dataframe(
        df_top[[
            'inscricao_estadual', 'valor_devido', 'dias_cobranca',
            'score', 'qtd_outliers'
        ]],
        hide_index=True,
        column_config={
            'inscricao_estadual': 'IE',
            'valor_devido': st.column_config.NumberColumn(
                'Valor Devido',
                format="R$ %.2f"
            ),
            'dias_cobranca': 'Dias',
            'score': st.column_config.NumberColumn('Score', format="%.1f"),
            'qtd_outliers': 'Severidade'
        },
        height=500
    )

# =============================================================================
# 13. ANÁLISE TEMPORAL
# =============================================================================

def render_analise_temporal(dados):
    st.header("📉 Análise Temporal")
    
    df_master = dados.get('master', pd.DataFrame())
    
    if df_master.empty or 'data_inclusao_cobranca' not in df_master.columns:
        st.warning("Dados temporais não disponíveis")
        return
    
    # Converter data
    df_master['data'] = pd.to_datetime(df_master['data_inclusao_cobranca'], errors='coerce')
    df_master['ano_mes'] = df_master['data'].dt.to_period('M').astype(str)
    
    # Agrupar por mês
    temporal = df_master.groupby('ano_mes').agg({
        'inscricao_estadual': 'nunique',
        'valor_total_devido': 'sum'
    }).reset_index()
    
    temporal.columns = ['mes', 'empresas', 'valor']
    
    # Gráfico
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=temporal['mes'], y=temporal['valor']/1e6, name="Valor (R$ Mi)"),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=temporal['mes'], y=temporal['empresas'], 
                   name="Empresas", mode='lines+markers'),
        secondary_y=True
    )
    
    fig.update_layout(title="Evolução Temporal da Cobrança", hovermode='x unified')
    fig.update_xaxes(title_text="Período")
    fig.update_yaxes(title_text="Valor (R$ Milhões)", secondary_y=False)
    fig.update_yaxes(title_text="Empresas", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 14. MACHINE LEARNING
# =============================================================================

def render_machine_learning(dados):
    st.header("🤖 Análises Preditivas e Priorização Inteligente")
    
    df_score = dados.get('score', pd.DataFrame())
    df_master = dados.get('master', pd.DataFrame())
    df_comp = dados.get('componentes', pd.DataFrame())
    
    if df_score.empty or df_master.empty:
        st.warning("⚠️ Dados insuficientes para análise preditiva")
        return
    
    # Tabs para diferentes funcionalidades
    tabs = st.tabs([
        "🎯 Priorização por Lista de IEs",
        "📊 Modelo Preditivo Geral",
        "🔍 Análise de Propensão a Pagamento"
    ])
    
    # =========================================================================
    # TAB 1: PRIORIZAÇÃO POR LISTA DE IEs
    # =========================================================================
    with tabs[0]:
        st.subheader("🎯 Priorização Inteligente de Lista de Empresas")
        st.markdown("""
        **Como funciona:**
        1. Cole a lista de Inscrições Estaduais (uma por linha)
        2. O sistema analisa cada empresa usando múltiplos critérios
        3. Retorna um ranking de priorização: **maior probabilidade de pagamento** → **menor**
        """)
        
        # Input de IEs
        ies_input = st.text_area(
            "Cole a lista de Inscrições Estaduais (uma por linha):",
            height=200,
            placeholder="254000012\n254000023\n254000034\n..."
        )
        
        if st.button("🚀 Processar Lista e Gerar Ranking"):
            if not ies_input.strip():
                st.warning("⚠️ Por favor, insira ao menos uma IE")
                return
            
            # Processar IEs - normalizar removendo pontos, hífens e espaços
            ies_lista_original = [ie.strip() for ie in ies_input.split('\n') if ie.strip()]
            ies_lista_normalizada = [
                ie.replace('.', '').replace('-', '').replace('/', '').replace(' ', '').strip() 
                for ie in ies_lista_original
            ]
            
            st.info(f"📊 Processando {len(ies_lista_normalizada)} Inscrições Estaduais...")
            
            # Merge dos dados
            df_completo = df_master.merge(
                df_score,
                on=['inscricao_estadual', 'tipo_debito'],
                how='inner'
            )
            
            # Normalizar IEs do dataframe para comparação
            df_completo['ie_normalizada'] = df_completo['inscricao_estadual'].astype(str).str.replace(r'[.\-/\s]', '', regex=True)
            
            # Filtrar apenas as IEs da lista
            df_filtrado = df_completo[
                df_completo['ie_normalizada'].isin(ies_lista_normalizada)
            ].copy()
            
            if df_filtrado.empty:
                st.error("❌ Nenhuma IE da lista foi encontrada no sistema")
                
                # Mostrar diagnóstico
                with st.expander("🔍 Diagnóstico - Clique para ver detalhes"):
                    st.markdown("**IEs fornecidas (normalizadas):**")
                    st.write(ies_lista_normalizada[:10])  # Mostrar primeiras 10
                    
                    st.markdown("**Exemplos de IEs no sistema (normalizadas):**")
                    ies_sistema = df_completo['ie_normalizada'].head(10).tolist()
                    st.write(ies_sistema)
                    
                    st.markdown("**IEs originais fornecidas:**")
                    st.write(ies_lista_original[:10])
                    
                    st.markdown("**Exemplos de IEs no formato do sistema:**")
                    ies_sistema_original = df_completo['inscricao_estadual'].head(10).tolist()
                    st.write(ies_sistema_original)
                
                return
            
            st.success(f"✅ Encontradas {len(df_filtrado)} empresas na lista")
            
            # ===== ALGORITMO DE PRIORIZAÇÃO =====
            st.markdown("---")
            st.subheader("🧮 Calculando Score de Propensão a Pagamento...")
            
            # Calcular score de propensão (inverso do risco)
            df_filtrado['score_propensao'] = 0
            
            # 1. Histórico de contatos (30%)
            if 'qtd_total_contatos' in df_filtrado.columns:
                # Normalizar entre 0 e 30
                max_contatos = df_filtrado['qtd_total_contatos'].max()
                if max_contatos > 0:
                    df_filtrado['score_propensao'] += (
                        df_filtrado['qtd_total_contatos'] / max_contatos * 30
                    )
            
            # 2. Capacidade de pagamento (25%)
            if 'score_capacidade_pagamento' in df_filtrado.columns:
                df_filtrado['score_propensao'] += (
                    df_filtrado['score_capacidade_pagamento'] / 100 * 25
                )
            
            # 3. Histórico de pagamento (20%)
            if 'score_historico_pagamento' in df_filtrado.columns:
                df_filtrado['score_propensao'] += (
                    df_filtrado['score_historico_pagamento'] / 100 * 20
                )
            
            # 4. Responsividade (15%)
            if 'score_responsividade' in df_filtrado.columns:
                df_filtrado['score_propensao'] += (
                    df_filtrado['score_responsividade'] / 100 * 15
                )
            
            # 5. Viabilidade (10%) - quanto maior viabilidade, maior propensão
            if 'score_viabilidade_cobranca' in df_filtrado.columns:
                df_filtrado['score_propensao'] += (
                    df_filtrado['score_viabilidade_cobranca'] / 100 * 10
                )
            
            # Penalidades (reduzem propensão)
            if 'flag_falencia' in df_filtrado.columns:
                df_filtrado.loc[df_filtrado['flag_falencia'] == 1, 'score_propensao'] -= 20
            
            if 'flag_recuperacao_judicial' in df_filtrado.columns:
                df_filtrado.loc[df_filtrado['flag_recuperacao_judicial'] == 1, 'score_propensao'] -= 15
            
            if 'flag_devedor_contumaz' in df_filtrado.columns:
                df_filtrado.loc[df_filtrado['flag_devedor_contumaz'] == 1, 'score_propensao'] -= 10
            
            # Garantir score entre 0 e 100
            df_filtrado['score_propensao'] = df_filtrado['score_propensao'].clip(0, 100)
            
            # Classificar propensão
            df_filtrado['classificacao_propensao'] = pd.cut(
                df_filtrado['score_propensao'],
                bins=[0, 30, 50, 70, 100],
                labels=['🔴 Baixa', '🟡 Média', '🟢 Alta', '🟢🟢 Muito Alta']
            )
            
            # Ordenar por propensão (maior primeiro)
            df_ranking = df_filtrado.sort_values('score_propensao', ascending=False).reset_index(drop=True)
            df_ranking['ranking'] = range(1, len(df_ranking) + 1)
            
            # ===== EXIBIR RESULTADOS =====
            st.markdown("---")
            st.success("✅ Ranking de Priorização Concluído!")
            
            # Métricas resumo
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                muito_alta = len(df_ranking[df_ranking['classificacao_propensao'] == '🟢🟢 Muito Alta'])
                st.metric("🟢🟢 Muito Alta", muito_alta)
            
            with col2:
                alta = len(df_ranking[df_ranking['classificacao_propensao'] == '🟢 Alta'])
                st.metric("🟢 Alta", alta)
            
            with col3:
                media = len(df_ranking[df_ranking['classificacao_propensao'] == '🟡 Média'])
                st.metric("🟡 Média", media)
            
            with col4:
                baixa = len(df_ranking[df_ranking['classificacao_propensao'] == '🔴 Baixa'])
                st.metric("🔴 Baixa", baixa)
            
            # Tabela de ranking
            st.markdown("### 📊 Ranking Completo de Priorização")
            
            colunas_exibir = ['ranking', 'inscricao_estadual', 'razao_social', 
                             'valor_total_devido', 'score_propensao', 
                             'classificacao_propensao', 'porte_por_faturamento']
            
            # Filtrar colunas que existem
            colunas_disponiveis = [col for col in colunas_exibir if col in df_ranking.columns]
            
            st.dataframe(
                df_ranking[colunas_disponiveis],
                hide_index=True,
                column_config={
                    'ranking': st.column_config.NumberColumn('🏆 Ranking', format="%d"),
                    'inscricao_estadual': 'IE',
                    'razao_social': 'Razão Social',
                    'valor_total_devido': st.column_config.NumberColumn(
                        'Valor Devido',
                        format="R$ %.2f"
                    ),
                    'score_propensao': st.column_config.ProgressColumn(
                        'Score Propensão',
                        format="%.1f",
                        min_value=0,
                        max_value=100
                    ),
                    'classificacao_propensao': 'Classificação',
                    'porte_por_faturamento': 'Porte'
                },
                height=600
            )
            
            # Gráfico de distribuição
            st.markdown("---")
            st.subheader("📈 Distribuição de Propensão a Pagamento")
            
            fig = px.histogram(
                df_ranking,
                x='score_propensao',
                nbins=20,
                title="Distribuição dos Scores de Propensão",
                labels={'score_propensao': 'Score de Propensão', 'count': 'Quantidade'},
                color_discrete_sequence=['#1565C0']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Download do ranking
            st.markdown("---")
            csv = df_ranking[colunas_disponiveis].to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                "📥 Download Ranking Completo (CSV)",
                csv,
                f"ranking_priorizacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                key='download-ranking'
            )
            
            # Insights automáticos
            st.markdown("---")
            st.subheader("💡 Insights e Recomendações")
            
            # Verificar se temos a coluna de valor
            if 'valor_total_devido' in df_ranking.columns:
                valor_alta = df_ranking[df_ranking['score_propensao'] >= 70]['valor_total_devido'].sum()
                valor_media = df_ranking[(df_ranking['score_propensao'] >= 50) & 
                                        (df_ranking['score_propensao'] < 70)]['valor_total_devido'].sum()
                
                st.markdown(f"""
                **Análise Estratégica:**
                
                1. **Prioridade Máxima (Hoje):**
                   - Focar nas **{muito_alta + alta} empresas** com propensão Alta/Muito Alta
                   - Potencial de recuperação estimado: **R$ {valor_alta/1e6:.2f}M**
                
                2. **Médio Prazo (Esta Semana):**
                   - Trabalhar as **{media} empresas** com propensão Média
                   - Valor em jogo: **R$ {valor_media/1e6:.2f}M**
                
                3. **Atenção Especial:**
                   - **{baixa} empresas** com baixa propensão requerem análise jurídica
                   - Considerar inscrição em dívida ativa
                
                4. **Ações Recomendadas:**
                   - Contato imediato com TOP 10 do ranking
                   - Oferecer condições especiais para TOP 30
                   - Monitorar empresas com score entre 50-70
                """)
            else:
                st.markdown(f"""
                **Análise Estratégica:**
                
                1. **Prioridade Máxima (Hoje):**
                   - Focar nas **{muito_alta + alta} empresas** com propensão Alta/Muito Alta
                
                2. **Médio Prazo (Esta Semana):**
                   - Trabalhar as **{media} empresas** com propensão Média
                
                3. **Atenção Especial:**
                   - **{baixa} empresas** com baixa propensão requerem análise jurídica
                   - Considerar inscrição em dívida ativa
                
                4. **Ações Recomendadas:**
                   - Contato imediato com TOP 10 do ranking
                   - Oferecer condições especiais para TOP 30
                   - Monitorar empresas com score entre 50-70
                """)
    
    # =========================================================================
    # TAB 2: MODELO PREDITIVO GERAL
    # =========================================================================
    with tabs[1]:
        st.subheader("📊 Modelo Preditivo de Risco de Inadimplência")
        
        st.markdown("""
        Este modelo analisa o perfil completo das empresas no sistema para identificar 
        padrões de risco e prever probabilidades de inadimplência.
        """)
        
        # Preparar dados para análise
        if df_score.empty or df_master.empty:
            st.warning("⚠️ Dados insuficientes para análise")
            return
        
        # Merge completo
        df_analise = df_master.merge(
            df_score[['inscricao_estadual', 'tipo_debito', 'score_final_priorizacao',
                     'classificacao_prioridade', 'score_capacidade_pagamento',
                     'score_historico_pagamento', 'score_responsividade']],
            on=['inscricao_estadual', 'tipo_debito'],
            how='inner'
        )
        
        # Tabs internas
        sub_tabs = st.tabs([
            "📈 Análise de Risco Geral",
            "🎯 Segmentação por Porte",
            "🏭 Análise Setorial",
            "📊 Matriz de Risco"
        ])
        
        # SUB-TAB 1: Análise de Risco Geral
        with sub_tabs[0]:
            st.markdown("### 📊 Distribuição de Risco no Portfólio")
            
            # Métricas principais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                risco_critico = len(df_analise[df_analise['classificacao_prioridade'] == 'PRIORIDADE_MAXIMA'])
                pct_critico = (risco_critico / len(df_analise)) * 100
                st.metric("🔴 Risco Crítico", f"{risco_critico:,}", f"{pct_critico:.1f}%")
            
            with col2:
                risco_alto = len(df_analise[df_analise['classificacao_prioridade'] == 'PRIORIDADE_ALTA'])
                pct_alto = (risco_alto / len(df_analise)) * 100
                st.metric("🟠 Risco Alto", f"{risco_alto:,}", f"{pct_alto:.1f}%")
            
            with col3:
                risco_medio = len(df_analise[df_analise['classificacao_prioridade'] == 'PRIORIDADE_MEDIA'])
                pct_medio = (risco_medio / len(df_analise)) * 100
                st.metric("🟡 Risco Médio", f"{risco_medio:,}", f"{pct_medio:.1f}%")
            
            with col4:
                risco_baixo = len(df_analise[df_analise['classificacao_prioridade'] == 'PRIORIDADE_BAIXA'])
                pct_baixo = (risco_baixo / len(df_analise)) * 100
                st.metric("🟢 Risco Baixo", f"{risco_baixo:,}", f"{pct_baixo:.1f}%")
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribuição de score
                fig = px.histogram(
                    df_analise,
                    x='score_final_priorizacao',
                    nbins=30,
                    title="Distribuição do Score de Priorização",
                    labels={'score_final_priorizacao': 'Score', 'count': 'Quantidade'},
                    color_discrete_sequence=['#1565C0']
                )
                fig.add_vline(x=df_analise['score_final_priorizacao'].mean(), 
                             line_dash="dash", line_color="red",
                             annotation_text="Média")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Valor por nível de risco
                if 'valor_total_devido' in df_analise.columns:
                    valor_por_risco = df_analise.groupby('classificacao_prioridade')['valor_total_devido'].sum().reset_index()
                    valor_por_risco.columns = ['Risco', 'Valor']
                    
                    fig = px.bar(
                        valor_por_risco,
                        x='Risco',
                        y='Valor',
                        title="Valor Total por Nível de Risco",
                        color='Risco',
                        color_discrete_map={
                            'PRIORIDADE_MAXIMA': '#d32f2f',
                            'PRIORIDADE_ALTA': '#f57c00',
                            'PRIORIDADE_MEDIA': '#fbc02d',
                            'PRIORIDADE_BAIXA': '#388e3c'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Análise de concentração
            st.markdown("---")
            st.markdown("### 📊 Análise de Concentração de Risco")
            
            if 'valor_total_devido' in df_analise.columns:
                # Top 10% dos débitos
                df_sorted = df_analise.sort_values('valor_total_devido', ascending=False)
                top_10_pct = int(len(df_sorted) * 0.1)
                valor_top_10 = df_sorted.head(top_10_pct)['valor_total_devido'].sum()
                valor_total = df_sorted['valor_total_devido'].sum()
                concentracao = (valor_top_10 / valor_total) * 100
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Concentração Top 10%", f"{concentracao:.1f}%")
                
                with col2:
                    st.metric("Valor Top 10%", f"R$ {valor_top_10/1e6:.2f}M")
                
                with col3:
                    mediana = df_analise['valor_total_devido'].median()
                    st.metric("Valor Mediano", formatar_moeda(mediana))
        
        # SUB-TAB 2: Segmentação por Porte
        with sub_tabs[1]:
            st.markdown("### 🎯 Análise de Risco por Porte da Empresa")
            
            if 'porte_por_faturamento' in df_analise.columns:
                # Agrupar por porte
                porte_analise = df_analise.groupby('porte_por_faturamento').agg({
                    'inscricao_estadual': 'nunique',
                    'valor_total_devido': 'sum',
                    'score_final_priorizacao': 'mean'
                }).reset_index()
                
                porte_analise.columns = ['Porte', 'Empresas', 'Valor Total', 'Score Médio']
                
                # Calcular risco por porte
                risco_porte = df_analise.groupby(['porte_por_faturamento', 'classificacao_prioridade']).size().reset_index(name='count')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(
                        risco_porte,
                        x='porte_por_faturamento',
                        y='count',
                        color='classificacao_prioridade',
                        title="Distribuição de Risco por Porte",
                        labels={'porte_por_faturamento': 'Porte', 'count': 'Quantidade'},
                        color_discrete_map={
                            'PRIORIDADE_MAXIMA': '#d32f2f',
                            'PRIORIDADE_ALTA': '#f57c00',
                            'PRIORIDADE_MEDIA': '#fbc02d',
                            'PRIORIDADE_BAIXA': '#388e3c'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.scatter(
                        porte_analise,
                        x='Empresas',
                        y='Score Médio',
                        size='Valor Total',
                        hover_data=['Porte'],
                        title="Empresas vs Score Médio por Porte",
                        color='Score Médio',
                        color_continuous_scale='RdYlGn_r'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Tabela resumo
                st.markdown("---")
                st.dataframe(
                    porte_analise,
                    hide_index=True,
                    column_config={
                        'Porte': 'Porte da Empresa',
                        'Empresas': 'Qtd Empresas',
                        'Valor Total': st.column_config.NumberColumn(
                            'Valor Total',
                            format="R$ %.2f"
                        ),
                        'Score Médio': st.column_config.NumberColumn(
                            'Score Médio',
                            format="%.1f"
                        )
                    }
                )
        
        # SUB-TAB 3: Análise Setorial
        with sub_tabs[2]:
            st.markdown("### 🏭 Análise de Risco por Setor Econômico")
            
            if 'secao_cnae' in df_analise.columns:
                # Top 10 setores
                setor_analise = df_analise.groupby('secao_cnae').agg({
                    'inscricao_estadual': 'nunique',
                    'valor_total_devido': 'sum',
                    'score_final_priorizacao': 'mean'
                }).reset_index()
                
                setor_analise.columns = ['Setor', 'Empresas', 'Valor Total', 'Score Médio']
                setor_analise = setor_analise.sort_values('Valor Total', ascending=False).head(10)
                
                # Gráfico de setores
                fig = px.bar(
                    setor_analise,
                    x='Setor',
                    y='Valor Total',
                    color='Score Médio',
                    title="Top 10 Setores - Valor em Cobrança",
                    labels={'Valor Total': 'Valor (R$)', 'Score Médio': 'Score'},
                    color_continuous_scale='RdYlGn_r'
                )
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Matriz setor x risco
                st.markdown("---")
                st.markdown("#### 📊 Matriz Setor x Nível de Risco")
                
                matriz_setor = df_analise.groupby(['secao_cnae', 'classificacao_prioridade']).size().reset_index(name='count')
                matriz_pivot = matriz_setor.pivot(index='secao_cnae', 
                                                  columns='classificacao_prioridade', 
                                                  values='count').fillna(0)
                
                fig = px.imshow(
                    matriz_pivot,
                    labels=dict(x="Nível de Risco", y="Setor CNAE", color="Quantidade"),
                    title="Mapa de Calor: Setores vs Risco",
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # SUB-TAB 4: Matriz de Risco
        with sub_tabs[3]:
            st.markdown("### 📊 Matriz de Risco Multidimensional")
            
            if all(col in df_analise.columns for col in ['score_capacidade_pagamento', 'score_historico_pagamento']):
                # Criar matriz
                fig = px.scatter(
                    df_analise.sample(min(1000, len(df_analise))),  # Sample para performance
                    x='score_capacidade_pagamento',
                    y='score_historico_pagamento',
                    color='classificacao_prioridade',
                    size='valor_total_devido',
                    hover_data=['inscricao_estadual', 'razao_social'],
                    title="Matriz: Capacidade de Pagamento vs Histórico",
                    labels={
                        'score_capacidade_pagamento': 'Capacidade de Pagamento',
                        'score_historico_pagamento': 'Histórico de Pagamento'
                    },
                    color_discrete_map={
                        'PRIORIDADE_MAXIMA': '#d32f2f',
                        'PRIORIDADE_ALTA': '#f57c00',
                        'PRIORIDADE_MEDIA': '#fbc02d',
                        'PRIORIDADE_BAIXA': '#388e3c'
                    }
                )
                
                # Adicionar linhas de referência
                fig.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5)
                fig.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Quadrantes
                st.markdown("---")
                st.markdown("#### 🎯 Análise por Quadrantes")
                
                # Definir quadrantes
                df_analise['quadrante'] = 'Outros'
                mask_q1 = (df_analise['score_capacidade_pagamento'] >= 50) & (df_analise['score_historico_pagamento'] >= 50)
                mask_q2 = (df_analise['score_capacidade_pagamento'] < 50) & (df_analise['score_historico_pagamento'] >= 50)
                mask_q3 = (df_analise['score_capacidade_pagamento'] < 50) & (df_analise['score_historico_pagamento'] < 50)
                mask_q4 = (df_analise['score_capacidade_pagamento'] >= 50) & (df_analise['score_historico_pagamento'] < 50)
                
                df_analise.loc[mask_q1, 'quadrante'] = 'Q1: Alta Cap + Bom Histórico'
                df_analise.loc[mask_q2, 'quadrante'] = 'Q2: Baixa Cap + Bom Histórico'
                df_analise.loc[mask_q3, 'quadrante'] = 'Q3: Baixa Cap + Mal Histórico'
                df_analise.loc[mask_q4, 'quadrante'] = 'Q4: Alta Cap + Mal Histórico'
                
                quadrante_stats = df_analise.groupby('quadrante').agg({
                    'inscricao_estadual': 'nunique',
                    'valor_total_devido': 'sum'
                }).reset_index()
                
                col1, col2, col3, col4 = st.columns(4)
                
                for idx, (col, q) in enumerate(zip([col1, col2, col3, col4], 
                                                   ['Q1: Alta Cap + Bom Histórico', 
                                                    'Q2: Baixa Cap + Bom Histórico',
                                                    'Q3: Baixa Cap + Mal Histórico',
                                                    'Q4: Alta Cap + Mal Histórico'])):
                    with col:
                        q_data = quadrante_stats[quadrante_stats['quadrante'] == q]
                        if not q_data.empty:
                            qtd = q_data.iloc[0]['inscricao_estadual']
                            valor = q_data.iloc[0]['valor_total_devido'] / 1e6
                            st.metric(q, f"{qtd:,}", f"R$ {valor:.1f}M")
                
                # Recomendações por quadrante
                st.markdown("---")
                st.markdown("#### 💡 Estratégias Recomendadas por Quadrante")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    **Q1 - Alta Capacidade + Bom Histórico** 🟢
                    - Prioridade para negociação facilitada
                    - Oferecer condições atrativas
                    - Foco em relacionamento
                    
                    **Q3 - Baixa Capacidade + Mal Histórico** 🔴
                    - Avaliar viabilidade jurídica
                    - Considerar execução fiscal
                    - Monitorar para inscrição em dívida ativa
                    """)
                
                with col2:
                    st.markdown("""
                    **Q2 - Baixa Capacidade + Bom Histórico** 🟡
                    - Parcelamento de longo prazo
                    - Acompanhamento próximo
                    - Apoio para recuperação
                    
                    **Q4 - Alta Capacidade + Mal Histórico** 🟠
                    - Investigar razões da inadimplência
                    - Pressão para regularização
                    - Possível má-fé ou desvio
                    """)
    
    # =========================================================================
    # TAB 3: ANÁLISE DE PROPENSÃO
    # =========================================================================
    with tabs[2]:
        st.subheader("🔍 Análise Detalhada de Propensão a Pagamento")
        
        st.markdown("""
        ### Fatores Considerados no Score:
        
        **Fatores Positivos (aumentam propensão):**
        - ✅ Histórico de contatos responsivos (30%)
        - ✅ Capacidade de pagamento comprovada (25%)
        - ✅ Histórico positivo de pagamentos (20%)
        - ✅ Alta responsividade em negociações (15%)
        - ✅ Viabilidade de cobrança (10%)
        
        **Fatores Negativos (reduzem propensão):**
        - ❌ Empresa em falência (-20 pontos)
        - ❌ Recuperação judicial (-15 pontos)
        - ❌ Devedor contumaz (-10 pontos)
        
        ### Interpretação dos Scores:
        - **70-100 pontos:** 🟢🟢 Muito Alta - Contato imediato prioritário
        - **50-70 pontos:** 🟢 Alta - Abordar esta semana
        - **30-50 pontos:** 🟡 Média - Monitorar e contatar em 30 dias
        - **0-30 pontos:** 🔴 Baixa - Avaliar ação jurídica
        """)
        
        # Estatísticas gerais
        if not df_score.empty:
            st.markdown("---")
            st.subheader("📊 Estatísticas Gerais do Sistema")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'score_capacidade_pagamento' in df_score.columns:
                    fig = px.histogram(
                        df_score,
                        x='score_capacidade_pagamento',
                        nbins=30,
                        title="Distribuição - Capacidade de Pagamento"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'score_historico_pagamento' in df_score.columns:
                    fig = px.histogram(
                        df_score,
                        x='score_historico_pagamento',
                        nbins=30,
                        title="Distribuição - Histórico de Pagamento"
                    )
                    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 15. RELATÓRIOS
# =============================================================================

def render_relatorios(dados):
    st.header("📋 Relatórios Executivos")
    
    df_score = dados.get('score', pd.DataFrame())
    df_master = dados.get('master', pd.DataFrame())
    
    if df_score.empty:
        st.warning("Dados não disponíveis")
        return
    
    # Resumo executivo
    st.markdown("### 📊 Resumo Executivo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Empresas", f"{df_master['inscricao_estadual'].nunique():,}")
        st.metric("Total Débitos", f"{len(df_master):,}")
    
    with col2:
        valor_total = df_master['valor_total_devido'].sum() / 1e9
        st.metric("Valor Total", f"R$ {valor_total:.2f}B")
        
        valor_medio = df_master['valor_total_devido'].mean()
        st.metric("Valor Médio", formatar_moeda(valor_medio))
    
    with col3:
        prior_max = len(df_score[df_score['classificacao_prioridade'] == 'PRIORIDADE_MAXIMA'])
        st.metric("Prioridade Máxima", f"{prior_max:,}")
        
        prior_alta = len(df_score[df_score['classificacao_prioridade'] == 'PRIORIDADE_ALTA'])
        st.metric("Prioridade Alta", f"{prior_alta:,}")
    
    # Recomendações
    st.markdown("---")
    st.markdown("### 💡 Recomendações")
    st.markdown("""
    1. **Ação Imediata:** Focar em {prior_max} casos de prioridade máxima
    2. **Curto Prazo:** Abordar {prior_alta} casos de prioridade alta
    3. **Monitoramento:** Acompanhar evolução dos scores
    4. **Preventivo:** Contatar empresas com tendência de piora
    """.format(prior_max=prior_max, prior_alta=prior_alta))

# =============================================================================
# 16. EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    main()