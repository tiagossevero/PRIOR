# 💰 GECOB - Sistema de Priorização de Cobrança

Sistema inteligente de priorização de cobranças tributárias desenvolvido para a **Receita Estadual de Santa Catarina**.

![Version](https://img.shields.io/badge/version-1.4-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.0+-red)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Módulos e Análises](#módulos-e-análises)
- [Algoritmo de Priorização](#algoritmo-de-priorização)
- [Segurança](#segurança)
- [Contribuindo](#contribuindo)

---

## 🎯 Sobre o Projeto

O **GECOB** é um dashboard interativo desenvolvido em Python que utiliza técnicas de Machine Learning e análise de dados para otimizar o processo de cobrança tributária. O sistema analisa múltiplos fatores para classificar débitos por ordem de prioridade, maximizando a eficiência da recuperação de créditos tributários.

### Objetivos Principais

- **Priorização Inteligente**: Classificação automática de débitos por níveis de prioridade
- **Análise Preditiva**: Identificação de empresas com maior propensão ao pagamento
- **Visualização de Dados**: Dashboards interativos para gestão e tomada de decisão
- **Otimização de Recursos**: Direcionamento eficiente das equipes de cobrança

---

## ✨ Funcionalidades

### 📊 Visão Geral
- KPIs principais (total de empresas, débitos, valor total)
- Distribuição por níveis de prioridade
- Top 10 maiores débitos
- Métricas em tempo real

### 🎯 Top Prioridades
- Ranking de empresas por score de priorização
- Filtros por nível de prioridade
- Exportação de relatórios em CSV
- Visualização customizável (top 10 a 100 registros)

### 🔍 Consulta Empresa
- Busca por Inscrição Estadual (IE)
- Perfil completo da empresa
- Análise detalhada dos componentes do score
- Gráfico radar dos 7 componentes de avaliação
- Histórico de contatos e situação cadastral

### 📈 Análise Setorial
- Distribuição por seção CNAE
- Top 10 setores por valor em cobrança
- Correlação entre setor e score médio
- Identificação de setores críticos

### 🗺️ Análise Geográfica
- Distribuição de débitos por município
- Top 15 municípios em cobrança
- Concentração geográfica de risco
- Mapas de calor regionais

### 👥 Análise de Clusters
- Segmentação de empresas por perfil
- Características de cada cluster
- Distribuição de valores e scores
- Estratégias específicas por grupo

### ⚠️ Outliers e Casos Críticos
- Identificação de casos atípicos
- Top 30 outliers mais críticos
- Análise de severidade
- Alertas de alto risco

### 📉 Análise Temporal
- Evolução histórica da cobrança
- Tendências mensais e anuais
- Sazonalidade de débitos
- Projeções futuras

### 🤖 Machine Learning

#### 🎯 Priorização por Lista de IEs
- **Entrada**: Lista de Inscrições Estaduais
- **Processo**: Análise multifatorial automatizada
- **Saída**: Ranking de priorização (maior → menor propensão de pagamento)
- **Uso**: Ideal para planejamento de rotinas de cobrança

#### 📊 Modelo Preditivo Geral
- Análise de risco de inadimplência
- Segmentação por porte e setor
- Matriz de risco multidimensional
- Quadrantes estratégicos de ação

#### 🔍 Análise de Propensão a Pagamento
- Score de 0-100 pontos
- Classificação: Baixa, Média, Alta, Muito Alta
- Fatores positivos e negativos
- Recomendações automáticas

### 📋 Relatórios
- Resumos executivos
- Indicadores de performance
- Recomendações estratégicas
- Exportação de dados

---

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.8+**: Linguagem principal
- **Streamlit**: Framework de dashboard interativo
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica

### Visualização
- **Plotly**: Gráficos interativos
- **Plotly Express**: Visualizações rápidas
- **Plotly Graph Objects**: Gráficos customizados

### Banco de Dados
- **SQLAlchemy**: ORM e conexão com banco
- **Impala**: Data warehouse (Apache Impala)

### Segurança
- **Hashlib**: Criptografia de senhas
- **SSL**: Conexões seguras

---

## 📦 Requisitos

```
python>=3.8
streamlit>=1.0.0
pandas>=1.3.0
numpy>=1.21.0
plotly>=5.0.0
sqlalchemy>=1.4.0
impyla>=0.17.0
```

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd PRIOR
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração

### 1. Credenciais do Banco de Dados

Crie o arquivo `.streamlit/secrets.toml`:

```toml
[impala_credentials]
user = "seu_usuario"
password = "sua_senha"
```

### 2. Configuração de Senha

Edite a variável `SENHA` no arquivo `PRIOR.py`:

```python
SENHA = "sua_senha_aqui"
```

### 3. Variáveis de Conexão

Configure as variáveis de conexão no arquivo `PRIOR.py`:

```python
IMPALA_HOST = 'seu_host_impala'
IMPALA_PORT = 21050
DATABASE = 'nome_do_banco'
```

---

## 💻 Uso

### Executar o Dashboard

```bash
streamlit run PRIOR.py
```

O sistema será aberto automaticamente no navegador em `http://localhost:8501`

### Acesso ao Sistema

1. Ao abrir, será solicitada a senha configurada
2. Após autenticação, o dashboard principal será exibido
3. Use o menu lateral para navegar entre as análises

### Exemplo de Uso - Priorização por Lista

1. Acesse **🤖 Machine Learning** → **🎯 Priorização por Lista de IEs**
2. Cole a lista de IEs (uma por linha):
   ```
   254000012
   254000023
   254000034
   ```
3. Clique em **🚀 Processar Lista e Gerar Ranking**
4. Analise o ranking gerado (ordenado por propensão de pagamento)
5. Exporte o relatório em CSV para ação da equipe

---

## 📁 Estrutura do Projeto

```
PRIOR/
│
├── PRIOR.py                           # Aplicação principal Streamlit
├── PRIOR COBR (6).ipynb              # Notebook de análise completa
├── PRIOR COBR-exemplo (2).ipynb      # Notebook de exemplos
├── PRIOR. COBRANÇA.json              # Dados de configuração
├── README.md                         # Este arquivo
│
├── .streamlit/
│   └── secrets.toml                  # Credenciais (não versionado)
│
└── requirements.txt                  # Dependências do projeto
```

---

## 🧮 Módulos e Análises

### 1. Carregamento de Dados

```python
@st.cache_data(ttl=3600)
def carregar_dados_gecob()
```

Carrega dados das seguintes tabelas:
- `prior_master_consolidado`: Dados mestres das empresas
- `prior_score_priorizacao`: Scores calculados
- `prior_score_componentes`: Componentes individuais
- `prior_clusters_empresas`: Segmentação por clusters
- `prior_outliers_identificados`: Casos atípicos

### 2. Componentes do Score

O sistema utiliza **7 componentes** para calcular o score final:

1. **Score Valor do Débito** (peso variável)
   - Considera o montante devido
   - Normalizado por faixas de valor

2. **Score Capacidade de Pagamento** (25%)
   - Análise de faturamento
   - Situação patrimonial
   - Porte da empresa

3. **Score Histórico de Pagamento** (20%)
   - Pagamentos anteriores
   - Regularidade
   - Atrasos históricos

4. **Score Responsividade** (15%)
   - Atendimento a contatos
   - Retorno de comunicações
   - Engajamento em negociações

5. **Score Viabilidade de Cobrança** (10%)
   - Situação cadastral
   - Existência de bens
   - Localização física

6. **Score Urgência** (peso variável)
   - Tempo de cobrança
   - Proximidade de prescrição
   - Prioridades legais

7. **Score Conformidade** (peso variável)
   - Situação legal
   - Regularidade fiscal
   - Obrigações acessórias

### 3. Classificação de Prioridade

Após o cálculo, os débitos são classificados em:

| Prioridade | Score | Cor | Ação Recomendada |
|-----------|-------|-----|------------------|
| PRIORIDADE_MAXIMA | 80-100 | 🔴 Vermelho | Ação imediata |
| PRIORIDADE_ALTA | 60-79 | 🟠 Laranja | Ação em 7 dias |
| PRIORIDADE_MEDIA | 40-59 | 🟡 Amarelo | Ação em 30 dias |
| PRIORIDADE_BAIXA | 0-39 | 🟢 Verde | Monitoramento |

---

## 🤖 Algoritmo de Priorização

### Score de Propensão a Pagamento

O algoritmo calcula um score de 0-100 que indica a probabilidade de pagamento:

#### Fatores Positivos (somam pontos)

```python
# 1. Histórico de Contatos (30%)
score += (qtd_contatos / max_contatos) * 30

# 2. Capacidade de Pagamento (25%)
score += (score_capacidade / 100) * 25

# 3. Histórico de Pagamento (20%)
score += (score_historico / 100) * 20

# 4. Responsividade (15%)
score += (score_responsividade / 100) * 15

# 5. Viabilidade (10%)
score += (score_viabilidade / 100) * 10
```

#### Penalidades (subtraem pontos)

```python
# Empresa em falência
if flag_falencia == 1:
    score -= 20

# Recuperação judicial
if flag_recuperacao_judicial == 1:
    score -= 15

# Devedor contumaz
if flag_devedor_contumaz == 1:
    score -= 10
```

### Classificação Final

| Score | Classificação | Ação |
|-------|--------------|------|
| 70-100 | 🟢🟢 Muito Alta | Contato imediato prioritário |
| 50-70 | 🟢 Alta | Abordar esta semana |
| 30-50 | 🟡 Média | Monitorar e contatar em 30 dias |
| 0-30 | 🔴 Baixa | Avaliar ação jurídica |

---

## 🔒 Segurança

### Autenticação

O sistema possui autenticação via senha na camada de apresentação:

```python
def check_password():
    # Validação de senha antes de acessar o sistema
    if senha_input == SENHA:
        st.session_state.authenticated = True
```

### Conexão Segura

- Conexões com banco de dados via SSL/TLS
- Credenciais armazenadas em `secrets.toml` (não versionado)
- Autenticação LDAP para Impala

### Boas Práticas

1. **Nunca commite** o arquivo `secrets.toml`
2. **Altere a senha padrão** em produção
3. **Use variáveis de ambiente** para dados sensíveis
4. **Mantenha** as dependências atualizadas

---

## 📊 Exemplos de Uso

### Consultar uma Empresa

```python
# Na interface, vá para "🔍 Consulta Empresa"
# Digite a IE: 254000012
# O sistema exibirá:
# - Dados cadastrais completos
# - Score de priorização
# - Gráfico radar dos componentes
# - Valor devido e composição (imposto, multa, juros)
```

### Gerar Ranking de Priorização

```python
# Na interface, vá para "🤖 Machine Learning"
# Cole lista de IEs:
254000012
254000023
254000034

# Clique em "Processar"
# Resultado: Ranking ordenado por propensão de pagamento
```

### Exportar Relatório

```python
# Em qualquer análise, use o botão "📥 Download CSV"
# O arquivo será salvo com timestamp:
# prioridades_20250116_143052.csv
```

---

## 🎨 Customização

### Alterar Cores do Dashboard

Edite o CSS no arquivo `PRIOR.py`:

```python
st.markdown("""
<style>
    .priority-max {
        background-color: #ffebee;
        border-left: 5px solid #c62828;
    }
</style>
""", unsafe_allow_html=True)
```

### Adicionar Nova Análise

1. Crie uma nova função `render_minha_analise(dados)`
2. Adicione a opção no menu lateral
3. Implemente a lógica de visualização

```python
def render_minha_analise(dados):
    st.header("📊 Minha Análise")
    # Sua implementação aqui
```

---

## 📈 Roadmap

- [ ] Integração com API de notificações
- [ ] Relatórios agendados automaticamente
- [ ] Dashboard mobile
- [ ] Exportação para PowerBI
- [ ] API REST para integração
- [ ] Análise de sentimento em histórico de contatos
- [ ] Previsão de arrecadação com ML

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é de propriedade da **Receita Estadual de Santa Catarina**.
Uso restrito para fins governamentais.

---

## 👥 Autores

**Receita Estadual de Santa Catarina**
Sistema GECOB - Gestão de Cobrança
Versão 1.4

---

## 📧 Contato

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento da Receita Estadual/SC.

---

## 🙏 Agradecimentos

- Equipe de Desenvolvimento da Receita Estadual/SC
- Equipe de Cobrança e Fiscalização
- Todos os colaboradores que contribuíram para o projeto

---

<div align="center">

**GECOB** - Sistema de Priorização de Cobrança
Desenvolvido com ❤️ pela Receita Estadual de Santa Catarina

</div>
