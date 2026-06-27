"""
Testes unitários para as funções de processamento de dados.

Não requerem banco de dados ou ambiente completo rodando,
pois testam a lógica isolada (ex: transformação pandas).
"""

import pandas as pd
from src.jobs.transform import _normalize_dataframe


def test_normalize_dataframe():
    """
    Testa se a função _normalize_dataframe processa corretamente
    os tipos de dados e strings conforme esperado.
    """
    # Dados brutos simulando a leitura do CSV original
    raw_data = {
        "cnpj_basico": ["123456", "12345678"],
        "razao_social": [" EMPRESA TESTE LTDA ", " OUTRA EMPRESA S.A."],
        "capital_social": ["1000,50", "250000,00"],
    }

    df_raw = pd.DataFrame(raw_data)

    # Aplica a transformação
    df_norm = _normalize_dataframe(df_raw)

    # Validações
    # 1. CNPJ Básico deve ter 8 dígitos (zero-padded)
    assert df_norm.iloc[0]["cnpj_basico"] == "00123456"
    assert df_norm.iloc[1]["cnpj_basico"] == "12345678"

    # 2. Razão Social deve estar sem espaços sobrando nas bordas
    assert df_norm.iloc[0]["razao_social"] == "EMPRESA TESTE LTDA"
    assert df_norm.iloc[1]["razao_social"] == "OUTRA EMPRESA S.A."

    # 3. Capital Social deve ser convertido para float (vírgula por ponto)
    assert df_norm.iloc[0]["capital_social"] == 1000.50
    assert df_norm.iloc[1]["capital_social"] == 250000.00
