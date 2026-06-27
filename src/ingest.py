import logging
import os
import zipfile
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

RAW_DIR = "./data/raw"
EXTRACT_DIR = "./data/extracted"


def extract_files():
    """
    Extrai todos os arquivos .zip encontrados em data/raw.
    """

    logger.info("Extraindo arquivos ZIP...")

    os.makedirs(EXTRACT_DIR, exist_ok=True)

    arquivos = [
        f for f in os.listdir(RAW_DIR)
        if f.endswith(".zip")
    ]

    if not arquivos:
        raise FileNotFoundError(
            "Nenhum arquivo .zip encontrado em data/raw."
        )

    for arquivo in arquivos:

        zip_path = os.path.join(RAW_DIR, arquivo)

        logger.info(f"Extraindo {arquivo}...")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)


def transform_empresas():

    logger.info("Transformando Empresas...")

    arquivos = sorted([
        f for f in os.listdir(EXTRACT_DIR)
        if f.endswith("EMPRECSV")
    ])

    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo de Empresas encontrado.")

    dfs = []

    for arquivo in arquivos:

        logger.info(f"Lendo {arquivo}")

        df = pd.read_csv(
            os.path.join(EXTRACT_DIR, arquivo),
            sep=";",
            encoding="latin1",
            header=None,
            nrows=1000
        )

        df.columns = [
            "cnpj_basico",
            "razao_social",
            "natureza_juridica",
            "qualificacao_responsavel",
            "capital_social",
            "porte_empresa",
            "ente_federativo"
        ]

        df["capital_social"] = (
            df["capital_social"]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )

        dfs.append(df)

    empresas = pd.concat(dfs, ignore_index=True)

    logger.info(f"{len(empresas)} empresas carregadas.")

    return empresas

def transform_estabelecimentos():

    logger.info("Transformando Estabelecimentos...")

    arquivos = sorted([
        f for f in os.listdir(EXTRACT_DIR)
        if f.endswith("ESTABELE")
    ])

    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo de Estabelecimentos encontrado.")

    dfs = []

    for arquivo in arquivos:

        logger.info(f"Lendo {arquivo}")

        df = pd.read_csv(
            os.path.join(EXTRACT_DIR, arquivo),
            sep=";",
            encoding="latin1",
            header=None,
            nrows=1000
        )

        dfs.append(df)

    estabelecimentos = pd.concat(dfs, ignore_index=True)

    logger.info(f"{len(estabelecimentos)} estabelecimentos carregados.")

    return estabelecimentos

def load_to_database(empresas, estabelecimentos):

    logger.info("Conectando ao PostgreSQL...")

    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@db:5432/cnpj"
    )

    empresas.to_sql(
        "empresas",
        engine,
        if_exists="replace",
        index=False
    )

    logger.info("Tabela empresas criada.")

    estabelecimentos.to_sql(
        "estabelecimentos",
        engine,
        if_exists="replace",
        index=False
    )

    logger.info("Tabela estabelecimentos criada.")


def run_pipeline():

    logger.info("Pipeline iniciado...")

    extract_files()

    empresas = transform_empresas()

    estabelecimentos = transform_estabelecimentos()

    load_to_database(
        empresas,
        estabelecimentos
    )

    logger.info("Pipeline concluído com sucesso!")


if __name__ == "__main__":
    run_pipeline()