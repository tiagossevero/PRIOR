# 💰 GECOB v2.0 - Sistema de Priorização de Cobrança

**Receita Estadual de Santa Catarina**
Sistema Analítico de Priorização de Cobrança Tributária

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![Status](https://img.shields.io/badge/status-production-success.svg)

---

## 📋 Índice

- [Sobre](#sobre)
- [Novidades v2.0](#novidades-v20)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura de Dados](#estrutura-de-dados)
- [Visualizações](#visualizações)
- [Performance](#performance)
- [Roadmap](#roadmap)

---

## 🎯 Sobre

O **GECOB (Gestão Estratégica de Cobrança)** é um sistema inteligente de priorização de cobranças tributárias que utiliza machine learning e análise multivariada para otimizar a recuperação de créditos da Fazenda Estadual de Santa Catarina.

### Objetivo

Maximizar a eficiência da cobrança tributária através de:
- **Priorização inteligente** baseada em 7 componentes de score
- **Análises preditivas** de propensão a pagamento
- **Insights automáticos** para tomada de decisão
- **Visualizações avançadas** do portfólio de cobrança

---

## 🎉 Novidades v2.0

### ✨ Destaques da Versão

1. **🏠 Dashboard Executivo** - Visão estratégica consolidada com KPIs avançados
2. **📊 Análise de Pareto** - Identificação automática da concentração 80/20
3. **🤖 Insights Automáticos** - Sistema inteligente de detecção de oportunidades
4. **📈 Estatísticas Expandidas** - Análises descritivas completas
5. **🎨 Design Modernizado** - Interface com gradientes e animações
6. **🔗 Heatmaps de Correlação** - Análise multivariada de componentes

### 📊 Números da v2.0

- **14 seções** analíticas (vs 10 anteriores)
- **9 KPIs** principais (vs 4 anteriores)
- **4+ insights** automáticos
- **15+ visualizações** interativas
- **100% compatível** com versão anterior

---

## 🚀 Funcionalidades

### 1. Dashboard Executivo

#### Indicadores Principais
```
🏢 Empresas    📋 Débitos    💰 Valor Total    📊 Score Médio    💵 Valor Médio
📊 Mediana     📈 Desvio     🔝 Maior Débito   📞 Total Contatos
```

#### Análises Visuais
- **Distribuição por Prioridade** - Pie chart com 4 níveis
- **Top 20 Maiores Débitos** - Ranking visual
- **Distribuição de Scores** - Histograma com estatísticas
- **Análise Setorial** - Top 15 setores econômicos
- **Análise Geográfica** - Top 15 municípios

#### Insights Automáticos
```python
✅ Oportunidades Identificadas
⚠️ Alta Concentração de Risco
🔴 Casos Críticos Detectados
📞 Empresas Sem Contato
```

#### Análise de Pareto
- Curva 80/20 interativa
- Identificação automática de concentração
- Recomendações estratégicas

### 2. Visão Geral Expandida

#### Estatísticas Descritivas
- Média, Mediana, Moda
- Desvio Padrão e Variância
- Quartis (Q1, Q2, Q3)
- Intervalo Interquartil (IQR)
- Mínimo e Máximo
- Outliers identificados

#### Visualizações
- **Box Plots** - Distribuição de valores e scores
- **Heatmap de Correlação** - Entre componentes de score
- **Análise por Porte** - Segmentação por tamanho
- **Gráficos de Componentes** - Média de cada score

### 3. Sistema de Priorização

#### Algoritmo Multi-Componente (7 Scores)

```
1. 💰 Score Valor do Débito (peso variável)
   - Montante devido normalizado

2. 💪 Score Capacidade de Pagamento (25%)
   - Análise de receita e ativos
   - Porte da empresa

3. 📊 Score Histórico de Pagamento (20%)
   - Regularidade de pagamentos
   - Atrasos anteriores

4. 📞 Score Responsividade (15%)
   - Retorno a contatos
   - Engajamento em negociações

5. ✅ Score Viabilidade de Cobrança (10%)
   - Situação cadastral
   - Existência de ativos

6. ⏰ Score Urgência (peso variável)
   - Tempo em cobrança
   - Proximidade de prescrição

7. 📋 Score Conformidade (peso variável)
   - Situação legal
   - Obrigações acessórias
```

#### Classificação de Prioridade

```
🔴 PRIORIDADE MÁXIMA (80-100)
   → Ação imediata requerida

🟠 PRIORIDADE ALTA (60-79)
   → Ação em 7 dias

🟡 PRIORIDADE MÉDIA (40-59)
   → Ação em 30 dias

🟢 PRIORIDADE BAIXA (0-39)
   → Monitoramento
```

### 4. Top Prioridades

- **Filtros dinâmicos** por nível de prioridade
- **Ranking ajustável** (10-200 registros)
- **Visualização detalhada** com todos os dados
- **Exportação CSV** com timestamp

### 5. Consulta Detalhada de Empresa

- **Busca por IE** com normalização automática
- **Perfil completo** da empresa
- **Gráfico radar** de componentes de score
- **Histórico de contatos**
- **Flags de risco** (falência, recuperação judicial)

### 6. Machine Learning (v1.4 - Mantido)

#### Priorização por Lista de IEs
```
Input: Lista de inscrições estaduais
Output: Ranking por propensão a pagamento

Algoritmo:
- Histórico de contatos (30%)
- Capacidade de pagamento (25%)
- Histórico de pagamento (20%)
- Responsividade (15%)
- Viabilidade (10%)
- Penalidades: falência (-20), RJ (-15), devedor contumaz (-10)
```

#### Classificação de Propensão
```
🟢🟢 Muito Alta (70-100): Contato imediato
🟢 Alta (50-70): Contato esta semana
🟡 Média (30-50): Monitorar e contatar em 30 dias
🔴 Baixa (0-30): Avaliar ação jurídica
```

---

## 🏗️ Arquitetura

### Tecnologias Principais

```
Frontend:  Streamlit
Backend:   Python 3.8+
Database:  Apache Impala
Cache:     Streamlit Cache
Viz:       Plotly Express / Plotly Graph Objects
ML:        scikit-learn, scipy
```

### Estrutura de Código

```
PRIOR.py
├── 1. Configurações e Autenticação
├── 2. CSS Customizado
├── 3. Credenciais e Conexão
├── 4. Funções de Carregamento
├── 5. Funções Auxiliares
├── 6. Interface Principal
├── 7. Dashboard Executivo (NOVO)
├── 8. Visão Geral Expandida
├── 9-14. Outras Seções
└── 15. Execução Principal
```

### Fluxo de Dados

```
Apache Impala
     ↓
Carregamento (com cache 1h)
     ↓
5 Tabelas principais
     ↓
Processamento e Análise
     ↓
Visualizações Interativas
     ↓
Dashboard Streamlit
```

---

## 📦 Instalação

### Pré-requisitos

```bash
Python >= 3.8
pip >= 20.0
```

### Dependências

```bash
pip install streamlit pandas numpy plotly sqlalchemy impyla scipy scikit-learn
```

### Configuração

1. **Criar arquivo de secrets:**
```bash
mkdir -p .streamlit
touch .streamlit/secrets.toml
```

2. **Configurar credenciais:**
```toml
[impala_credentials]
user = "seu_usuario"
password = "sua_senha"
```

3. **Executar aplicação:**
```bash
streamlit run PRIOR.py
```

---

## 💻 Uso

### Acesso

1. Abra o navegador em `http://localhost:8501`
2. Digite a senha de acesso
3. Navegue pelas seções no menu lateral

### Navegação

```
🏠 Dashboard Executivo
   └─ Visão consolidada e KPIs principais

📊 Visão Geral Expandida
   └─ Estatísticas e distribuições

🎯 Top Prioridades
   └─ Ranking de ação prioritária

🔍 Consulta Detalhada
   └─ Busca individual por IE

📈 Análise Setorial
   └─ Segmentação por CNAE

🗺️ Análise Geográfica
   └─ Distribuição por município

👥 Análise de Clusters
   └─ Segmentação por perfil

⚠️ Outliers e Casos Críticos
   └─ Casos atípicos

📉 Análise Temporal
   └─ Evolução histórica

🤖 Machine Learning
   └─ Modelos preditivos
```

### Exportações

- **CSV:** Tabelas de prioridades e rankings
- **Dados:** Disponíveis em dataframes
- **Visualizações:** Plotly permite salvar imagens

---

## 📊 Estrutura de Dados

### Tabelas do Sistema

#### 1. prior_master_consolidado
```
Campos principais:
- inscricao_estadual (PK)
- tipo_debito (PK)
- razao_social
- nome_municipio
- porte_por_faturamento
- valor_total_devido
- secao_cnae
- situacao_cadastral_desc
- qtd_total_contatos
- flags: falencia, recuperacao_judicial, devedor_contumaz
- saldos: imposto, multa, juros
```

#### 2. prior_score_priorizacao
```
Campos principais:
- inscricao_estadual (PK)
- tipo_debito (PK)
- score_final_priorizacao (0-100)
- classificacao_prioridade
- 7 scores componentes
```

#### 3. prior_score_componentes
```
Detalhamento dos componentes de score
```

#### 4. prior_clusters_empresas
```
Segmentação por perfil comportamental
```

#### 5. prior_outliers_identificados
```
Casos atípicos e críticos
```

---

## 📈 Visualizações

### Tipos de Gráficos

1. **Pie Charts** - Distribuição de categorias
2. **Bar Charts** - Rankings e comparações
3. **Line Charts** - Evolução temporal
4. **Scatter Plots** - Correlações bivariadas
5. **Box Plots** - Distribuições e outliers
6. **Histogramas** - Frequências
7. **Heatmaps** - Matrizes de correlação
8. **Radar Charts** - Componentes multidimensionais
9. **Gauge Charts** - Medidores de performance
10. **Pareto Charts** - Análise 80/20

### Paleta de Cores

```
Prioridades:
🔴 Máxima: #d32f2f (vermelho)
🟠 Alta:   #f57c00 (laranja)
🟡 Média:  #fbc02d (amarelo)
🟢 Baixa:  #388e3c (verde)

Gradientes principais:
Principal: #667eea → #764ba2 (roxo/azul)
Sucesso:   #e8f5e9 → #c8e6c9 (verde)
Alerta:    #fff3e0 → #ffe0b2 (laranja)
Perigo:    #ffebee → #ffcdd2 (vermelho)
```

---

## ⚡ Performance

### Otimizações

- **Cache de dados:** 1 hora TTL
- **Queries otimizadas:** SELECT apenas colunas necessárias
- **Lazy loading:** Carregamento sob demanda
- **Sampling:** Visualizações com amostragem quando necessário

### Métricas Esperadas

```
Tempo de carregamento inicial: 5-15s
Navegação entre seções:       <1s
Renderização de gráficos:     <2s
Exportação CSV:                <3s
```

---

## 🗺️ Roadmap

### ✅ Concluído (v2.0)

- [x] Dashboard Executivo
- [x] Análise de Pareto
- [x] Insights Automáticos
- [x] Estatísticas Expandidas
- [x] Heatmap de Correlação
- [x] Design Modernizado

### 🚧 Em Desenvolvimento

- [ ] Análise Setorial Avançada
- [ ] Análise Temporal com Forecasting
- [ ] Análise de Correlação Multivariada
- [ ] Machine Learning Avançado

### 📅 Futuro (v3.0)

- [ ] Simulador de Cenários
- [ ] Sistema de Alertas Inteligentes
- [ ] Relatórios Executivos PDF
- [ ] API REST
- [ ] Dashboard Mobile
- [ ] Integração BI Externo

---

## 📄 Licença

Propriedade da Receita Estadual de Santa Catarina.
Uso interno restrito.

---

## 👥 Suporte

Para questões técnicas ou sugestões:
- Entre em contato com a equipe de desenvolvimento
- Consulte a documentação interna
- Verifique os logs de carregamento no sistema

---

## 📚 Documentação Adicional

- [CHANGELOG v2.0](CHANGELOG_v2.0.md) - Lista completa de mudanças
- Documentação técnica das tabelas (interno)
- Manual de uso detalhado (interno)

---

**💰 GECOB v2.0 - Cobrança Inteligente e Eficiente**

*Desenvolvido com ❤️ para a Receita Estadual de Santa Catarina*
