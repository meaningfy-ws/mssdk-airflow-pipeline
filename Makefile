SHELL=/bin/bash -o pipefail

BUILD_PRINT = \e[1;34m
END_BUILD_PRINT = \e[0m

ICON_DONE = [✔]
ICON_ERROR = [x]
ICON_WARNING = [!]
ICON_PROGRESS = [-]

ENV_FILE := .env
-include .env

PROJECT_PATH = $(shell pwd)

RML_MAPPER_PROJ_DIR = ${PROJECT_PATH}/.rmlmapper
AIRFLOW_PROJ_DIR = ${PROJECT_PATH}/infra/airflow/.airflow
OPEN_TELEMETRY_PROJ_DIR = ${PROJECT_PATH}/infra/open-telemetry/.open-telemetry

RML_MAPPER_PATH = ${RML_MAPPER_PROJ_DIR}/rmlmapper.jar

build: guard-ENVIRONMENT guard-SUBDOMAIN guard-ENV_FILE create-env-airflow create-env-marquez init-rml-mapper
	@ docker-compose -p ${ENVIRONMENT}-${SUBDOMAIN} --file ./infra/docker-compose.yaml --env-file ${ENV_FILE} up -d --force-recreate --build

build-%: guard-ENVIRONMENT guard-SUBDOMAIN guard-ENV_FILE create-env-airflow create-env-marquez init-rml-mapper
	@ docker-compose -p ${ENVIRONMENT}-${SUBDOMAIN} --file ./infra/docker-compose.yaml --env-file ${ENV_FILE} up -d --force-recreate --build $*

create-env-marquez: guard-PROJECT_PATH
	@ chmod 777 ${PROJECT_PATH}/infra/marquez/wait-for-it.sh

create-env-airflow: guard-PROJECT_PATH guard-AIRFLOW_PROJ_DIR guard-ENVIRONMENT init-rml-mapper
	@ echo -e "$(BUILD_PRINT)$(ICON_PROGRESS) Creating/Updating Airflow environment $(END_BUILD_PRINT)"
	@ echo -e "$(BUILD_PRINT) ${AIRFLOW_PROJ_DIR} ${ENVIRONMENT} $(END_BUILD_PRINT)"
	@ rm -rf ${AIRFLOW_PROJ_DIR} && mkdir -p ${AIRFLOW_PROJ_DIR}

	@ chmod 777 ${AIRFLOW_PROJ_DIR}
	@ chmod 777 ${PROJECT_PATH}/requirements.txt
	@ chmod 777 ${PROJECT_PATH}/.env

	@ mkdir -p ${AIRFLOW_PROJ_DIR}/logs
	@ mkdir -p ${AIRFLOW_PROJ_DIR}/config
	@ mkdir -p ${AIRFLOW_PROJ_DIR}/plugins

	@ mkdir -p ${PROJECT_PATH}/dags/sources
	@ mkdir -p ${PROJECT_PATH}/dags/sources/input_mp
	@ mkdir -p ${PROJECT_PATH}/dags/sources/input_notice
	@ mkdir -p ${PROJECT_PATH}/dags/sources/output_rdf

#	@ uv pip compile pyproject.toml -o ${AIRFLOW_PROJ_DIR}/requirements.txt > /dev/null
#	@ ln -s -f -n ${PROJECT_PATH}/requirements.txt ${AIRFLOW_PROJ_DIR}/requirements.txt
	@ cp ${PROJECT_PATH}/requirements.txt ${AIRFLOW_PROJ_DIR}
	@ ln -s -f -n ${PROJECT_PATH}/.env ${AIRFLOW_PROJ_DIR}/.env
	@ ln -s -f -n ${PROJECT_PATH}/dags ${AIRFLOW_PROJ_DIR}/dags
	@ ln -s -f -n ${PROJECT_PATH}/.rmlmapper ${AIRFLOW_PROJ_DIR}/.rmlmapper
	@ ln -s -f -n ${PROJECT_PATH}/mssdk_airflow_pipeline ${AIRFLOW_PROJ_DIR}/mssdk_airflow_pipeline

	@ echo -e "$(BUILD_PRINT)$(ICON_DONE) Creating/Updating Airflow environment done$(END_BUILD_PRINT)"

init-rml-mapper:
	@ echo -e "$(BUILD_PRINT)$(ICON_PROGRESS) Checking RML Mapper $(END_BUILD_PRINT)"
	@ mkdir -p $(RML_MAPPER_PROJ_DIR)
	@ if [ ! -f "$(RML_MAPPER_PATH)" ]; then \
	    echo -e "$(BUILD_PRINT)$(ICON_PROGRESS) Downloading RML Mapper $(END_BUILD_PRINT)"; \
	    wget -c https://github.com/RMLio/rmlmapper-java/releases/download/v6.2.2/rmlmapper-6.2.2-r371-all.jar -O $(RML_MAPPER_PATH); \
	    chmod 777 $(RML_MAPPER_PATH); \
	    echo -e "$(BUILD_PRINT)$(ICON_DONE) Downloading RML Mapper done $(END_BUILD_PRINT)"; \
	else \
	    echo -e "$(BUILD_PRINT)$(ICON_WARNING) RML Mapper already exists, skipping download $(END_BUILD_PRINT)"; \
	fi

guard-%:
	@ if [ "${${*}}" = "" ]; then \
        echo -e "$(BUILD_PRINT)$(ICON_ERROR) Environment variable $* not set. Please set .env file $(END_BUILD_PRINT)"; \
        exit 1; \
	fi


.PHONY: build build-% create-env-airflow init-rml-mapper guard-%