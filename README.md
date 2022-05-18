# finapp

Welcome to your finapp repository.

### Contents

| Name | Description |
|-|-|
| `config/` | directory that contains the config files for deployment regarding to the enviroment |
| `finapp/` | A Python module that contains code of finapp application |
| `finapp_tests/` | A Python module that contains tests for `finapp` |
| `README.md` | A description and guide for this code repository |
| `setup.py` | A build script with Python package dependencies for this code repository |


## General architecture

![image](src/images/architecture_diagram.png).

## Prerequisites
 * Docker
 * get sandbox_api_key by open an account in [finhub](https://finnhub.io/)

## How to use
 * create a .env file in the main folder with this env variables.
```Bash
FINNUB_KEY=your_sandbox_api_key
DAGSTER_PG_USERNAME=<admin_db_name>
DAGSTER_PG_PASSWORD=<admin_db_pwd>
DAGSTER_PG_HOST=finapp_db_backend #no modify this
DAGSTER_PG_DB=<db_name>
DAGSTER_PG_OP_DB=<db_operational_db>
DAGSTER_PG_OP_DB_PORT=5433 #no modify this
DAGSTER_CURRENT_IMAGE=finapp_pipelines #no modify this
```
 * Build the container images with `docker compose build`
 * Run the container with `docker compose up`
   * If you want it running in the background, use `docker compose up -d`