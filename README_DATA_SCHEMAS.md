# 📊 Gerador Automático de Data Schemas - GECOB

## 🎯 Arquivo Principal

**`GERAR_DATA_SCHEMAS.ipynb`** - Notebook completo e auto-contido para gerar schemas das tabelas GECOB

---

## 🚀 Como Usar

### 1️⃣ Abrir o notebook

```bash
jupyter notebook GERAR_DATA_SCHEMAS.ipynb
```

### 2️⃣ Executar as células na ordem

1. **Célula 1-2**: Configurações e imports
2. **Célula 3**: Criar SparkSession (escolha uma das opções)
3. **Célula 4**: Verificar acesso às tabelas
4. **Células 5-7**: Definir funções auxiliares
5. **Célula 8**: ⭐ **EXECUTAR O GERADOR** (principal)
6. **Células 9-14**: Visualizar resultados e exportar

### 3️⃣ Pronto!

Os arquivos estarão em `data_schemas/`

---

## 📋 O que será gerado?

### Para cada uma das 5 tabelas:

✅ `{tabela}_describe_formatted.csv` - Schema completo
✅ `{tabela}_describe_formatted.json` - Schema em JSON
✅ `{tabela}_describe_formatted.md` - Schema em Markdown
✅ `{tabela}_sample_10.csv` - Amostra de 10 registros
✅ `{tabela}_sample_10.json` - Amostra em JSON
✅ `{tabela}_sample_10.md` - Amostra em Markdown

### Arquivos consolidados:

✅ `README.md` - Índice dos schemas
✅ `data_schemas_completo.json` - JSON com tudo

**Total:** 31 arquivos

---

## 📊 Tabelas Processadas

1. `gecob.prior_master_consolidado`
2. `gecob.prior_score_priorizacao`
3. `gecob.prior_score_componentes`
4. `gecob.prior_clusters_empresas`
5. `gecob.prior_outliers_identificados`

---

## ✨ Diferenciais

### ✅ Sem conflito com PySpark

O notebook foi desenvolvido para **evitar o erro `PySparkTypeError`** que ocorre quando `sum()` do Python é sobrescrito por `pyspark.sql.functions.sum()`.

**Solução implementada:**
- Uso de `len()` explicitamente
- Compreensões de lista ao invés de `sum()`
- Import de `builtins` quando necessário

### ✅ Auto-contido

Não depende de arquivos `.py` externos - tudo está no notebook.

### ✅ Completo

Inclui:
- Setup do Spark
- Verificação de acesso
- Geração dos schemas
- Visualização dos resultados
- Export para ZIP

---

## 🔧 Customizações

Edite a **Célula 1 (Configurações)** para alterar:

```python
DATABASE = 'gecob'           # Database
TABELAS = [...]              # Lista de tabelas
OUTPUT_DIR = 'data_schemas'  # Diretório de saída
SAMPLE_LIMIT = 10            # Registros no sample
```

---

## 📁 Estrutura de Saída

```
data_schemas/
├── README.md
├── data_schemas_completo.json
├── prior_master_consolidado_describe_formatted.csv
├── prior_master_consolidado_describe_formatted.json
├── prior_master_consolidado_describe_formatted.md
├── prior_master_consolidado_sample_10.csv
├── prior_master_consolidado_sample_10.json
├── prior_master_consolidado_sample_10.md
├── (... arquivos das outras 4 tabelas ...)
```

---

## ⚠️ Requisitos

- ✅ Acesso ao ambiente Spark (Jupyter com PySpark)
- ✅ Permissão para ler tabelas `gecob.*`
- ✅ Libs: `pyspark`, `pandas`, `json`, `os`

---

## 💡 Dicas

1. **Execute célula por célula** na primeira vez para entender o processo
2. **Verifique a célula 4** antes de prosseguir (teste de acesso)
3. **A célula 8 demora** alguns minutos (processa 5 tabelas)
4. **Use a célula 14** para gerar um ZIP com tudo

---

## 📧 Suporte

Em caso de dúvidas:

1. Leia os comentários no notebook
2. Veja os notebooks de exemplo: `PRIOR COBR (6).ipynb`
3. Confira `COMO_USAR_GERADOR_SCHEMAS.md`

---

## ✅ Checklist

- [ ] Abri o notebook `GERAR_DATA_SCHEMAS.ipynb`
- [ ] Executei a célula de configurações
- [ ] Executei a célula de imports
- [ ] Criei a SparkSession
- [ ] Verifiquei acesso às tabelas (célula 4)
- [ ] Executei o gerador (célula 8)
- [ ] Verifiquei os arquivos em `data_schemas/`
- [ ] (Opcional) Criei o ZIP

---

**GECOB - Sistema de Priorização de Cobrança**
Receita Estadual de Santa Catarina
