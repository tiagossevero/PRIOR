# 📖 Como Usar o Gerador de Data Schemas

Guia rápido para gerar automaticamente os data schemas das tabelas GECOB.

---

## 🎯 O que o script faz?

O script **`gerar_data_schemas.py`** gera automaticamente para cada tabela:

1. ✅ **DESCRIBE FORMATTED** - Schema completo da tabela
2. ✅ **SELECT * FROM ... LIMIT 10** - Amostra de 10 registros
3. ✅ **COUNT(*)** - Total de registros
4. ✅ Exporta tudo em **CSV, JSON e Markdown**

---

## 📋 Tabelas Documentadas

O script processa estas 5 tabelas:

1. `gecob.prior_master_consolidado`
2. `gecob.prior_score_priorizacao`
3. `gecob.prior_score_componentes`
4. `gecob.prior_clusters_empresas`
5. `gecob.prior_outliers_identificados`

---

## 🚀 Opção 1: Usar o Notebook (RECOMENDADO)

### Passo a Passo:

1. **Abra o notebook:**
   ```bash
   jupyter notebook EXECUTAR_gerar_schemas.ipynb
   ```

2. **Execute as células na ordem:**
   - Célula 1: Imports
   - Célula 2: Criar SparkSession
   - Célula 3: Verificar acesso às tabelas
   - Célula 4: **EXECUTAR O GERADOR** ⭐
   - Célula 5+: Ver resultados

3. **Pronto!** Os arquivos estarão em `data_schemas/`

---

## 🐍 Opção 2: Usar Direto no Notebook (Rápido)

Se você já tem uma SparkSession ativa em um notebook:

```python
# Importar o script
import gerar_data_schemas

# Executar (assumindo que 'spark' está disponível)
gerar_data_schemas.main(spark)
```

Ou usando `%run`:

```python
%run gerar_data_schemas.py
main(spark)
```

---

## 🐍 Opção 3: Script Python Standalone

Se preferir rodar como script Python:

```python
from pyspark.sql import SparkSession
import gerar_data_schemas

# Criar SparkSession
spark = SparkSession.builder \
    .appName("Gerar Data Schemas") \
    .enableHiveSupport() \
    .getOrCreate()

# Executar
gerar_data_schemas.main(spark)

# Finalizar
spark.stop()
```

---

## 📁 Arquivos Gerados

Após a execução, você terá:

```
data_schemas/
├── README.md                                         # Índice dos schemas
├── data_schemas_completo.json                        # JSON consolidado
│
├── prior_master_consolidado_describe_formatted.csv   # Schema em CSV
├── prior_master_consolidado_describe_formatted.json  # Schema em JSON
├── prior_master_consolidado_describe_formatted.md    # Schema em Markdown
├── prior_master_consolidado_sample_10.csv            # Amostra em CSV
├── prior_master_consolidado_sample_10.json           # Amostra em JSON
├── prior_master_consolidado_sample_10.md             # Amostra em Markdown
│
├── prior_score_priorizacao_describe_formatted.csv
├── prior_score_priorizacao_describe_formatted.json
├── prior_score_priorizacao_describe_formatted.md
├── prior_score_priorizacao_sample_10.csv
├── prior_score_priorizacao_sample_10.json
├── prior_score_priorizacao_sample_10.md
│
├── prior_score_componentes_describe_formatted.csv
├── prior_score_componentes_describe_formatted.json
├── prior_score_componentes_describe_formatted.md
├── prior_score_componentes_sample_10.csv
├── prior_score_componentes_sample_10.json
├── prior_score_componentes_sample_10.md
│
├── prior_clusters_empresas_describe_formatted.csv
├── prior_clusters_empresas_describe_formatted.json
├── prior_clusters_empresas_describe_formatted.md
├── prior_clusters_empresas_sample_10.csv
├── prior_clusters_empresas_sample_10.json
├── prior_clusters_empresas_sample_10.md
│
├── prior_outliers_identificados_describe_formatted.csv
├── prior_outliers_identificados_describe_formatted.json
├── prior_outliers_identificados_describe_formatted.md
├── prior_outliers_identificados_sample_10.csv
├── prior_outliers_identificados_sample_10.json
└── prior_outliers_identificados_sample_10.md
```

**Total:** 31 arquivos (1 README + 1 JSON consolidado + 6 arquivos × 5 tabelas)

---

## 📊 Formatos Disponíveis

### CSV (`.csv`)
- ✅ Fácil de importar no Excel, Google Sheets
- ✅ Codificação UTF-8 com BOM
- ✅ Sem índice

### JSON (`.json`)
- ✅ Estruturado para APIs e programação
- ✅ Formato: `orient='records'`
- ✅ Indentação legível
- ✅ Caracteres especiais preservados

### Markdown (`.md`)
- ✅ Visualização bonita no GitHub
- ✅ Tabelas formatadas
- ✅ Timestamp de geração

### JSON Consolidado
- ✅ Um único arquivo com tudo
- ✅ Inclui metadata (timestamp, row count)
- ✅ Ideal para documentação automática

---

## 🔧 Customizações

### Alterar lista de tabelas

Edite o arquivo `gerar_data_schemas.py`:

```python
TABELAS = [
    'prior_master_consolidado',
    'prior_score_priorizacao',
    # Adicione ou remova tabelas aqui
    'minha_nova_tabela',
]
```

### Alterar database

```python
DATABASE = 'gecob'  # Altere para outro database
```

### Alterar número de registros no sample

```python
# Na função gerar_schema_tabela(), linha ~88:
df_sample = spark.sql(f"SELECT * FROM {DATABASE}.{tabela} LIMIT 10")
#                                                             ^^
#                                                       altere aqui
```

### Alterar diretório de saída

```python
OUTPUT_DIR = 'data_schemas'  # Altere para outro diretório
```

---

## ⚠️ Troubleshooting

### Erro: "SparkSession não encontrada"

**Problema:** Script executado fora de um ambiente Spark

**Solução:** Use o notebook ou crie uma SparkSession antes

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("test").getOrCreate()
```

---

### Erro: "Table not found: gecob.prior_master_consolidado"

**Problema:** Tabela não existe ou sem permissão

**Solução:** Verifique se você tem acesso:

```python
spark.sql("SHOW DATABASES").show()
spark.sql("SHOW TABLES IN gecob").show()
```

---

### Erro: "Permission denied: data_schemas/"

**Problema:** Sem permissão para criar diretório

**Solução:** Execute em um diretório onde você tem permissão de escrita

---

### Arquivo muito grande

**Problema:** Sample com muitas colunas gera arquivos grandes

**Solução:**
1. Reduza o LIMIT (de 10 para 5, por exemplo)
2. Selecione apenas colunas específicas
3. Use apenas formato CSV ou JSON (comente as outras linhas)

---

## 📞 Suporte

Em caso de dúvidas:

1. Veja os exemplos nos notebooks `PRIOR COBR (6).ipynb`
2. Confira a documentação do PySpark SQL
3. Verifique os logs de execução no terminal

---

## ✅ Checklist de Execução

- [ ] Tenho acesso ao ambiente Spark
- [ ] Tenho permissão para ler as tabelas `gecob.*`
- [ ] Abri o notebook `EXECUTAR_gerar_schemas.ipynb`
- [ ] Executei a célula de imports
- [ ] Criei a SparkSession
- [ ] Verifiquei acesso às tabelas
- [ ] Executei o gerador
- [ ] Verifiquei os arquivos em `data_schemas/`
- [ ] Li o `data_schemas/README.md`

---

**GECOB - Sistema de Priorização de Cobrança**
Receita Estadual de Santa Catarina
