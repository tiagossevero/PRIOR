#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar data schemas das tabelas GECOB
Gera DESCRIBE FORMATTED e SELECT * FROM ... LIMIT 10 para cada tabela
Autor: Receita Estadual SC - Sistema GECOB
Data: 2025-11-17
"""

import os
import json
from datetime import datetime

# ============================================================
# CONFIGURAÇÕES
# ============================================================

DATABASE = 'gecob'

# Lista de tabelas para documentar
TABELAS = [
    'prior_master_consolidado',
    'prior_score_priorizacao',
    'prior_score_componentes',
    'prior_clusters_empresas',
    'prior_outliers_identificados'
]

# Diretório de saída
OUTPUT_DIR = 'data_schemas'

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def criar_diretorio_output():
    """Cria diretório de saída se não existir"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✅ Diretório '{OUTPUT_DIR}' criado")
    else:
        print(f"📁 Diretório '{OUTPUT_DIR}' já existe")

def salvar_dataframe_como_json(df, nome_arquivo):
    """Salva DataFrame pandas como JSON"""
    caminho = os.path.join(OUTPUT_DIR, nome_arquivo)
    df.to_json(caminho, orient='records', indent=2, force_ascii=False)
    print(f"   💾 Salvo: {caminho}")

def salvar_dataframe_como_csv(df, nome_arquivo):
    """Salva DataFrame pandas como CSV"""
    caminho = os.path.join(OUTPUT_DIR, nome_arquivo)
    df.to_csv(caminho, index=False, encoding='utf-8-sig')
    print(f"   💾 Salvo: {caminho}")

def salvar_dataframe_como_markdown(df, nome_arquivo, titulo):
    """Salva DataFrame como tabela Markdown"""
    caminho = os.path.join(OUTPUT_DIR, nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(f"# {titulo}\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(df.to_markdown(index=False))
    print(f"   💾 Salvo: {caminho}")

# ============================================================
# FUNÇÕES PRINCIPAIS
# ============================================================

def gerar_schema_tabela(spark, tabela):
    """
    Gera schema completo de uma tabela

    Args:
        spark: SparkSession
        tabela: nome da tabela

    Returns:
        dict com metadata da tabela
    """
    print(f"\n{'='*60}")
    print(f"📊 Processando: {DATABASE}.{tabela}")
    print(f"{'='*60}")

    resultado = {
        'database': DATABASE,
        'tabela': tabela,
        'timestamp': datetime.now().isoformat(),
        'describe_formatted': None,
        'sample_data': None,
        'row_count': None
    }

    try:
        # 1. DESCRIBE FORMATTED
        print(f"\n🔍 Executando: DESCRIBE FORMATTED {DATABASE}.{tabela}")
        df_describe = spark.sql(f"DESCRIBE FORMATTED {DATABASE}.{tabela}").toPandas()
        resultado['describe_formatted'] = df_describe.to_dict('records')

        # Salvar describe
        salvar_dataframe_como_csv(df_describe, f"{tabela}_describe_formatted.csv")
        salvar_dataframe_como_json(df_describe, f"{tabela}_describe_formatted.json")
        salvar_dataframe_como_markdown(
            df_describe,
            f"{tabela}_describe_formatted.md",
            f"DESCRIBE FORMATTED {DATABASE}.{tabela}"
        )

        print(f"   ✅ Schema obtido: {len(df_describe)} linhas")

        # 2. SELECT * FROM ... LIMIT 10
        print(f"\n📋 Executando: SELECT * FROM {DATABASE}.{tabela} LIMIT 10")
        df_sample = spark.sql(f"SELECT * FROM {DATABASE}.{tabela} LIMIT 10").toPandas()
        resultado['sample_data'] = df_sample.to_dict('records')

        # Salvar sample
        salvar_dataframe_como_csv(df_sample, f"{tabela}_sample_10.csv")
        salvar_dataframe_como_json(df_sample, f"{tabela}_sample_10.json")
        salvar_dataframe_como_markdown(
            df_sample,
            f"{tabela}_sample_10.md",
            f"SELECT * FROM {DATABASE}.{tabela} LIMIT 10"
        )

        print(f"   ✅ Sample obtido: {len(df_sample)} registros x {len(df_sample.columns)} colunas")

        # 3. COUNT(*)
        print(f"\n🔢 Executando: SELECT COUNT(*) FROM {DATABASE}.{tabela}")
        df_count = spark.sql(f"SELECT COUNT(*) as total FROM {DATABASE}.{tabela}").toPandas()
        total_rows = df_count.iloc[0]['total']
        resultado['row_count'] = int(total_rows)

        print(f"   ✅ Total de registros: {total_rows:,}")

        # 4. Resumo da tabela
        print(f"\n📊 Resumo da tabela {tabela}:")
        print(f"   - Total de registros: {total_rows:,}")
        print(f"   - Total de colunas: {len(df_sample.columns)}")
        print(f"   - Colunas: {', '.join(df_sample.columns.tolist()[:10])}{'...' if len(df_sample.columns) > 10 else ''}")

        return resultado

    except Exception as e:
        print(f"   ❌ Erro ao processar {tabela}: {str(e)}")
        resultado['error'] = str(e)
        return resultado

def gerar_relatorio_consolidado(resultados):
    """Gera relatório consolidado de todas as tabelas"""
    print(f"\n{'='*60}")
    print(f"📄 Gerando relatório consolidado")
    print(f"{'='*60}")

    # Salvar JSON consolidado
    caminho_json = os.path.join(OUTPUT_DIR, 'data_schemas_completo.json')
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON consolidado salvo: {caminho_json}")

    # Criar README.md
    caminho_readme = os.path.join(OUTPUT_DIR, 'README.md')
    with open(caminho_readme, 'w', encoding='utf-8') as f:
        f.write("# Data Schemas - GECOB\n\n")
        f.write(f"**Database:** `{DATABASE}`\n\n")
        f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write("## 📊 Tabelas Documentadas\n\n")

        for r in resultados:
            if 'error' not in r:
                f.write(f"### {r['tabela']}\n\n")
                f.write(f"- **Total de registros:** {r['row_count']:,}\n")
                f.write(f"- **Arquivos gerados:**\n")
                f.write(f"  - `{r['tabela']}_describe_formatted.csv` - Schema completo\n")
                f.write(f"  - `{r['tabela']}_sample_10.csv` - Amostra de 10 registros\n")
                f.write(f"  - `{r['tabela']}_describe_formatted.json` - Schema em JSON\n")
                f.write(f"  - `{r['tabela']}_sample_10.json` - Amostra em JSON\n")
                f.write(f"  - `{r['tabela']}_describe_formatted.md` - Schema em Markdown\n")
                f.write(f"  - `{r['tabela']}_sample_10.md` - Amostra em Markdown\n")
                f.write("\n")
            else:
                f.write(f"### ❌ {r['tabela']}\n\n")
                f.write(f"**Erro:** {r['error']}\n\n")

        f.write("---\n\n")
        f.write("## 📁 Estrutura de Arquivos\n\n")
        f.write("```\n")
        f.write("data_schemas/\n")
        f.write("├── README.md                                    # Este arquivo\n")
        f.write("├── data_schemas_completo.json                   # JSON consolidado\n")
        for tabela in TABELAS:
            f.write(f"├── {tabela}_describe_formatted.csv\n")
            f.write(f"├── {tabela}_describe_formatted.json\n")
            f.write(f"├── {tabela}_describe_formatted.md\n")
            f.write(f"├── {tabela}_sample_10.csv\n")
            f.write(f"├── {tabela}_sample_10.json\n")
            f.write(f"└── {tabela}_sample_10.md\n")
        f.write("```\n")

    print(f"✅ README.md criado: {caminho_readme}")

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main(spark):
    """
    Função principal do script

    Args:
        spark: SparkSession ativa
    """
    print("="*60)
    print("🚀 GERADOR DE DATA SCHEMAS - GECOB")
    print("="*60)
    print(f"Database: {DATABASE}")
    print(f"Tabelas: {len(TABELAS)}")
    print(f"Output: ./{OUTPUT_DIR}/")
    print("="*60)

    # Criar diretório de saída
    criar_diretorio_output()

    # Processar cada tabela
    resultados = []
    for tabela in TABELAS:
        resultado = gerar_schema_tabela(spark, tabela)
        resultados.append(resultado)

    # Gerar relatório consolidado
    gerar_relatorio_consolidado(resultados)

    # Resumo final
    print(f"\n{'='*60}")
    print("✅ PROCESSO CONCLUÍDO!")
    print(f"{'='*60}")
    print(f"📊 Tabelas processadas: {len(resultados)}")

    sucesso = sum(1 for r in resultados if 'error' not in r)
    erro = len(resultados) - sucesso

    print(f"   ✅ Sucesso: {sucesso}")
    if erro > 0:
        print(f"   ❌ Erros: {erro}")

    print(f"\n📁 Arquivos gerados em: ./{OUTPUT_DIR}/")
    print(f"📄 Veja README.md para detalhes dos arquivos")
    print("="*60)

# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    print("\n⚠️  IMPORTANTE:")
    print("    Este script deve ser executado em um ambiente com SparkSession ativa")
    print("    Exemplo de uso no notebook:\n")
    print("    # 1. Importe o script")
    print("    import gerar_data_schemas")
    print("")
    print("    # 2. Execute passando a SparkSession")
    print("    gerar_data_schemas.main(spark)")
    print("")
    print("    # OU execute diretamente se tiver spark no contexto:")
    print("    %run gerar_data_schemas.py")
    print("    main(spark)")
    print("")
