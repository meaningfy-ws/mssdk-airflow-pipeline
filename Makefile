SHELL=/bin/bash -o pipefail

BUILD_PRINT = \e[1;34m
END_BUILD_PRINT = \e[0m

ICON_DONE = [✔]
ICON_ERROR = [x]
ICON_WARNING = [!]
ICON_PROGRESS = [-]

ENV_FILE := .env
-include .env

build: guard-ENVIRONMENT guard-ENV_FILE create-env-airflow create-env-marquez
	@ docker-compose -p ${ENVIRONMENT}-${SUBDOMAIN} --file ./infra/docker-compose.yaml --env-file ${ENV_FILE} up -d --force-recreate --build

build-%:
	@ docker-compose -p ${ENVIRONMENT}-${SUBDOMAIN} --file ./infra/docker-compose.yaml --env-file ${ENV_FILE} up -d --force-recreate --build $*

create-env-marquez: guard-PROJECT_PATH
	@ chmod 777 ${PROJECT_PATH}/infra/marquez/wait-for-it.sh

create-env-airflow: guard-PROJECT_PATH guard-AIRFLOW_PROJ_DIR guard-ENVIRONMENT
	@ echo -e "$(BUILD_PRINT)$(ICON_PROGRESS) Creating/Updating Airflow environment $(END_BUILD_PRINT)"
	@ echo -e "$(BUILD_PRINT) ${AIRFLOW_PROJ_DIR} ${ENVIRONMENT} $(END_BUILD_PRINT)"
	@ rm -rf ${AIRFLOW_PROJ_DIR} && mkdir ${AIRFLOW_PROJ_DIR}
	@ mkdir -p ${AIRFLOW_PROJ_DIR}/logs
	@ mkdir -p ${AIRFLOW_PROJ_DIR}/config
	@ mkdir -p ${AIRFLOW_PROJ_DIR}/plugins

	@ uv pip compile pyproject.toml -o ${AIRFLOW_PROJ_DIR}/requirements.txt > /dev/null
	@ ln -s -f ${PROJECT_PATH}/.env ${AIRFLOW_PROJ_DIR}/.env
	@ ln -s -f -n ${PROJECT_PATH}/dags ${AIRFLOW_PROJ_DIR}/dags

	@ chmod 777 ${AIRFLOW_PROJ_DIR}/.env
	@ chmod 777 ${AIRFLOW_PROJ_DIR}/requirements.txt

	@ echo -e "$(BUILD_PRINT)$(ICON_DONE) Creating/Updating Airflow environment done$(END_BUILD_PRINT)"


guard-%:
	@ if [ "${${*}}" = "" ]; then \
        echo -e "$(BUILD_PRINT)$(ICON_ERROR) Environment variable $* not set. Please set .env file $(END_BUILD_PRINT)"; \
        exit 1; \
	fi


.PHONY: build create-env-airflow guard-%