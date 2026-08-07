# Copilot Instructions

## Project Context: TechStack Compass

This project is an end-to-end Data Engineering and Machine Learning pipeline designed to extract tech job postings, model them as a Knowledge Graph, and predict high-value skills using Graph Neural Networks. The project is managed with uv.

## Core Technologies & Rules

You must strictly adhere to the following stack and conventions:

### 1. Data Engineering (Ingestion & Orchestration)

- *Tooling:* Python 3.12+, Apache Airflow, Podman (instead of Docker).

- *Libraries:* Use httpx for async API calls (prefer over requests), pandas for data manipulation, and SQLAlchemy for DB connections.

- *Rule:* Airflow DAGs must be idempotent. External API calls must handle rate limits and timeouts gracefully.

Adzuna rate limits:
- 25 hits per minute
- 250 hits per day
- 1000 hits per week
- 2500 hits per month

### 2. Data Transformation (dbt)

- *Tooling:* dbt (Data Build Tool) with PostgreSQL adapter.

- *Rule:* Write clean, modular ANSI SQL. Always use {{ ref() }} for dependencies.

- *Goal:* Transform raw job descriptions into 'Nodes' (Jobs, Skills) and 'Edges' (Co-occurrences) tables.

### 3. Machine Learning (Graph Neural Networks)

- *Tooling:* PyTorch, PyTorch Geometric (PyG).

- *Rule:* Prefer standard architectures (GraphSAGE, GCN) for Link Prediction tasks. Code must be device-agnostic (check for MPS/CUDA, fallback to CPU).

- *Goal:* Generate embeddings for skills to calculate optimal learning paths.

### 4. API & Backend (FastAPI + Vector DB)

- *Tooling:* FastAPI, Qdrant (or Milvus) for vector search.

- *Rule:* All endpoints must be async def. Use pydantic v2 for strict request/response validation.

- *Rule:* Ensure the API reads pre-computed embeddings from the Vector DB, avoiding heavy PyTorch inference at runtime.

### 5. General Coding Hygiene

- Always use Python type hints (def process_data(input: str) -> dict:).

- Document complex logic with concise docstrings.

- If suggesting shell commands, prefer podman and podman-compose over docker.

- Do not suggest monolithic functions. Break logic into testable components.

### 6. Project Structure Awareness

- When creating or modifying scripts, place them in the folder that matches their responsibility:
  - Data ingestion and orchestration logic in `airflow/` or `src/techstack_compass/data/`.
  - dbt models and SQL logic in `dbt/models/`, with macros in `dbt/macros/` and seeds in `dbt/seeds/`.
  - API endpoints and request/response handling in `src/techstack_compass/api/`.
  - Machine learning and graph-based logic in `src/techstack_compass/ml/`.
  - Shared utilities and configuration in `src/techstack_compass/core/`.
  - Tests in `tests/unit/` or `tests/integration/` depending on scope.

- Prefer keeping related functionality grouped by domain rather than creating ad-hoc files at the repository root.

- When generating new code, follow the existing tree and avoid introducing new top-level folders unless they are clearly justified by the project architecture.