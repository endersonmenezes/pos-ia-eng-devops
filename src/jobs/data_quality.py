import os
import sys
import logging
import great_expectations as gx
import great_expectations.expectations as gxe
from src.config import DATABASE_URL

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def run_data_quality_checks():
    """
    Roda verificações de qualidade de dados (Data Quality) no PostgreSQL 
    usando Great Expectations v1.0+.
    """
    logger.info("Inicializando contexto do Great Expectations (em memória)...")
    context = gx.get_context(mode="ephemeral")

    connection_string = DATABASE_URL
    if connection_string.startswith("postgresql://"):
        connection_string = connection_string.replace("postgresql://", "postgresql+psycopg2://", 1)

    # 1. Configurar Datasource
    datasource_name = "cnpj_postgres_db"
    datasource = context.data_sources.add_postgres(
        name=datasource_name,
        connection_string=connection_string
    )

    # 2. Configurar Assets e Batch Definitions
    asset_empresas = datasource.add_table_asset(name="asset_empresas", table_name="cnpj_empresas")
    batch_def_empresas = asset_empresas.add_batch_definition_whole_table("bd_empresas")

    asset_simples = datasource.add_table_asset(name="asset_simples", table_name="cnpj_simples")
    batch_def_simples = asset_simples.add_batch_definition_whole_table("bd_simples")

    # 3. Criar Expectation Suites separadas
    suite_empresas = gx.ExpectationSuite(name="empresas_suite")
    suite_empresas.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="cnpj_basico"))
    suite_empresas.add_expectation(gxe.ExpectColumnValueLengthsToEqual(column="cnpj_basico", value=8))
    suite_empresas = context.suites.add(suite_empresas)

    suite_simples = gx.ExpectationSuite(name="simples_suite")
    suite_simples.add_expectation(gxe.ExpectColumnValuesToBeInSet(column="opcao_pelo_simples", value_set=["S", "N", " ", ""]))
    suite_simples = context.suites.add(suite_simples)

    # 4. Configurar Validation Definitions
    vd_empresas = context.validation_definitions.add(
        gx.ValidationDefinition(name="vd_empresas", data=batch_def_empresas, suite=suite_empresas)
    )
    vd_simples = context.validation_definitions.add(
        gx.ValidationDefinition(name="vd_simples", data=batch_def_simples, suite=suite_simples)
    )

    # 5. Criar e rodar o Checkpoint
    checkpoint = gx.Checkpoint(
        name="cnpj_checkpoint",
        validation_definitions=[vd_empresas, vd_simples]
    )
    checkpoint = context.checkpoints.add(checkpoint)

    logger.info("Executando Checkpoint v1.0+...")
    result = checkpoint.run()

    if not result.success:
        logger.error("Falha nos testes de Qualidade de Dados (Great Expectations v1.0+).")
        logger.error("Resumo do resultado:")
        # Na versão 1.0, o print do result já traz um descritivo bom
        logger.error(str(result))
        sys.exit(1)

    logger.info("✅ Todos os Data Quality Checks passaram com sucesso!")

if __name__ == "__main__":
    run_data_quality_checks()
