#Variables
PYTHON_PATH_ENV_APP=$(shell which python)
SRC_DIR = src
DOCKER_COMPOSE = APP_DOCKER_COMMAND=$(APP_DOCKER_COMMAND) DOCKER_TARGET=$(DOCKER_TARGET) COMPOSE_FILE=$(COMPOSE_FILE) docker-compose
RUN_DOCKER_DEV = $(DOCKER_COMPOSE) up -d --remove-orphans
STOP_DOCKER_DEV = $(DOCKER_COMPOSE) down
KILL_DOCKER_DEV = $(DOCKER_COMPOSE) kill

LOGS_DOCKER_DEV = $(DOCKER_COMPOSE) logs
PRUNE_DOCKER = docker system prune -af


ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

run: ## run DB's inside docker and run django server in your host
	RUN_APP=false make run-docker
	$(RUN_CMD)
.PHONY: run

run-app: ## run django server in your host
	$(RUN_DOCKER_DEV)
	$(RUN_CMD)
.PHONY: run-app

stop-docker: ## stop docker containers
	$(STOP_DOCKER_DEV)
.PHONY: stop

kill-docker: ## stop dockers server in docker in dev mode
	$(KILL_DOCKER_DEV)
.PHONY: kill-docker

stop: | stop-docker kill kill-docker ## stop everything
	@echo "Everything stopped or killed"
.PHONY: stop

build-images: ## build docker containers
	docker-compose -f src/ms_orders/docker-compose.yml build --no-cache --force-rm 
	docker-compose -f src/ms_products/docker-compose.yml build --no-cache --force-rm 
	docker-compose -f src/ms_customers/docker-compose.yml build --no-cache --force-rm
	docker-compose -f k8s/monitoring/docker-compose.yml build --no-cache --force-rm
.PHONY: build-images

push-images: ## push docker images to custom docker registry
	docker tag ms_customers-api:latest us-west1-docker.pkg.dev/olist-cloud/olist-containers/ms_customers_api:latest
	docker push us-west1-docker.pkg.dev/olist-cloud/olist-containers/ms_customers_api:latest

	docker tag ms_products-api:latest us-west1-docker.pkg.dev/olist-cloud/olist-containers/ms_products_api:latest
	docker push us-west1-docker.pkg.dev/olist-cloud/olist-containers/ms_products_api:latest

	docker tag ms_orders-api:latest us-west1-docker.pkg.dev/olist-cloud/olist-containers/ms_orders_api:latest
	docker push us-west1-docker.pkg.dev/olist-cloud/olist-containers/ms_orders_api:latest

	docker tag ms_orders-api:latest us-west1-docker.pkg.dev/olist-cloud/olist-containers/monitoring:latest
	docker push us-west1-docker.pkg.dev/olist-cloud/olist-containers/monitoring:latest 
.PHONY: push-images

deploy: ## deploy servicestio k8s
	kubectl apply -f k8s/
	kubectl apply -f src/ms_orders/k8s/
	kubectl apply -f src/ms_products/k8s/
	kubectl apply -f src/ms_customers/k8s/
.PHONY: deploy

del-pods: ## delete pods
	kubectl delete -f k8s/
	kubectl delete --all pods
.PHONY: del-pods

del-deploy: ## delete deploy
	kubectl delete deployment --all
.PHONY: del-deploy

build-orders: ## build orders container
	docker-compose -f src/ms_orders/docker-compose.yml build --no-cache --force-rm 
.PHONY: build-orders

build-products: ## build products container
	docker-compose -f src/ms_products/docker-compose.yml build --no-cache --force-rm 
.PHONY: build-products

build-customers: ## build customers container
	docker-compose -f src/ms_customers/docker-compose.yml build --no-cache --force-rm
.PHONY: build-customers