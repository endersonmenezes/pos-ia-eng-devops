# Receita Federal CNPJ API

Projeto desenvolvido para a disciplina de DevOps aplicado à Engenharia de Dados.

## Objetivo

Disponibilizar uma API utilizando FastAPI e um ambiente containerizado com Podman Compose para processamento de dados públicos do CNPJ da Receita Federal.

## Tecnologias utilizadas

- Python 3.14
- FastAPI
- Podman
- Podman Compose
- PostgreSQL
- MinIO (S3 Compatível)

## Estrutura do projeto

```
.
|__ data/
|    |
|    |__ raw/
|    |  |
|    |  |__ empresas1.zip
|    |  |__ estabelecimentos1.zip
|    |   
|    |__ extracted/
|           
| 
|
├── src/
│   ├── main.py
│   └── ingest.py
├── ContainerFile
├── compose.yaml
├── requirements.txt
├── Makefile
├── README.md
└── .gitignore
```

## Como executar

Construir as imagens:

```bash
podman compose build
```

Iniciar os serviços:

```bash
podman compose up
```

Encerrar os serviços:

```bash
podman compose down
```

## Endpoints

- http://localhost:8000
- http://localhost:8000/docs
- http://localhost:8000/health