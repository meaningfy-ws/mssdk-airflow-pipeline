# MSSDK Airflow Pipeline

A data processing pipeline (PoC) for Notice transformation using Apache Airflow and RML Mapping technology.

## Overview

This project implements an ETL (Extract, Transform, Load) pipeline for processing notices using RML Mapping technology. The pipeline is orchestrated with Apache Airflow and includes the following components:

- **Extract**: Fetch notices from external APIs
- **Transform**: Apply RML Mapping to transform notices into RDF format
- **Load**: Store transformed data in MongoDB or other storage systems

## Features

- Data extraction from external APIs
- RML Mapping-based transformation of notices to RDF
- Orchestration of workflows using Apache Airflow
- Data lineage tracking with OpenLineage/Marquez
- Observability with OpenTelemetry
- Monitoring with Grafana

## Prerequisites

- Docker and Docker Compose
- Java (for RML Mapper)
- Python 3.12+

## Installation

1. Clone the repository:

```shell
git clone https://github.com/your-organization/mssdk-airflow-pipeline.git`

cd mssdk-airflow-pipeline
```

2. Create .env file with necessary environment variables:

```dotenv
ENVIRONMENT=mssdk
SUBDOMAIN=dev
DOMAIN=localhost
AIRFLOW_POSTGRES_USER=the_user
AIRFLOW_POSTGRES_PASSWORD=the_password
AIRFLOW_POSTGRES_DB_NAME=the_db
AIRFLOW_UID=1000
DAG_LOGGER_CONFIG_HANDLERS=
AIRFLOW__WEBSERVER__SECRET_KEY=addsufhq3049hfpas;dmfaps
GRAFANA_PORT=3000
PROMETHEUS_PORT=9090
AIRFLOW_PORT=8080
MARQUEZ_WEB_PORT=3000
MARQUEZ_DB_USER=marquez
MARQUEZ_DB_PASSWORD=marquez
MARQUEZ_DB_NAME=marquez
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
```

3. Build and start the infrastructure:

```shell
make build
```

## Usage

1. Access the Airflow UI at http://localhost:8080 (default credentials: airflow/airflow)

2. To run the notice transformation pipeline:
- Place mapping packages in `dags/sources/input_mp/`
- Place notice XML files in `dags/sources/input_notice/`
- Trigger the `transformation_dag` in Airflow UI
- Transformed RDF will be available in `dags/sources/output_rdf/`

## DAGs

- **extract_notices_from_api**: Extracts notices from an external API
- **process_notices**: Processes notices from MongoDB
- **transformation_dag**: Transforms notice XML to RDF using RML mapping
- **postgres_dag**: Example DAG for PostgreSQL operations

