# Hooper Airflow

Este repositório contém DAGs e pipelines para processamento de dados meteorológicos usando Airflow.

> **Nota:** Este repositório contém o frontend do projeto Hopper. Os repositórios dos componentes principais estão separados:

- Backend (API + autenticação): https://github.com/until99/hopper-api
- Frontend (aplicação): https://github.com/until99/hopper-app
- Hopper (Landing Page): https://github.com/until99/hopper

## Estrutura principal

- `dags/` — arquivos de DAG do Apache Airflow (ponto principal para criar/editar workflows).
- `pipelines/` — módulos e utilitários que executam o processamento (separação de responsabilidades).
- `config/` — arquivos de configuração (ex.: `airflow.cfg`).
- `logs/` — diretórios de logs gerados pelo Airflow (útil para depuração local).
- `plugins/` — plugins personalizados do Airflow.
- `docker-compose.yaml` — definição de serviços para executar o ambiente local (Airflow, banco, etc.).
- `pyproject.toml` — metadados do Python / dependências (projeto gerenciado via Poetry ou similar).

## Requisitos

- Docker Desktop (ou engine Docker) instalado
- Docker Compose (v2 integrado ao `docker` é recomendado)

> Observação: o Docker Compose cuida das dependências do Airflow e dos serviços auxiliares — é a maneira recomendada para setup local.

## Rodando localmente (com Docker Compose)

Abra um terminal na raiz do projeto e execute:

```bash
# builda e sobe os serviços em primeiro plano
docker compose up --build

# para rodar em background (detached)
docker compose up --build -d

# ver logs
docker compose logs -f

# parar e remover containers
docker compose down
```

Dica rápida: a primeira inicialização pode demorar (build e pull de imagens). Após a inicialização, você deve conseguir acessar a UI do Airflow conforme definido no `docker-compose.yaml` (verifique a porta mapeada no arquivo).

Nota: o projeto fornece `pyproject.toml`; ajuste os comandos acima conforme seu fluxo (Poetry, pip, pip-tools, etc.).

## Como navegar rapidamente

- Para adicionar/editar DAGs: abra `dags/`.
- Para lógica de processamento e helpers: `pipelines/`.
- Para configuração do Airflow: `config/airflow.cfg`.
- Logs gerados localmente ficam em `logs/`.
