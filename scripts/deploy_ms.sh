#!/bin/bash

# Configure your shell to use the same Docker as Minikube
eval $(minikube docker-env)

# Constroi imagens Docker para cada serviço
docker-compose -f ../src/ms_orders/docker-compose.yml build
docker-compose -f ../src/ms_products/docker-compose.yml build
docker-compose -f ../src/ms_customers/docker-compose.yml build

# Iniciar os containers para cada serviço
docker-compose -f ../src/ms_orders/docker-compose.yml up -d
docker-compose -f ../src/ms_products/docker-compose.yml up -d
docker-compose -f ../src/ms_customers/docker-compose.yml up -d

# Aguardar alguns segundos para os containers inicializarem completamente
sleep 10

# Executar migrações de banco de dados (substitua este comando pelo comando real de migração)
python ../src/ms_orders/utils/parse_dataset.py
python ../src/ms_products/utils/parse_dataset.py
python ../src/ms_customers/utils/parse_dataset.py

echo "Building and deployment completed successfully."


kubectl apply -f ../src/ms_orders/k8s/deployment.yaml
kubectl apply -f ../src/ms_orders/k8s/ms-orders-hpa.yaml
kubectl apply -f ../src/ms_products/k8s/deployment.yaml
kubectl apply -f ../src/ms_products/k8s/ms-products-hpa.yaml
kubectl apply -f ../src/ms_customers/k8s/deployment.yaml
kubectl apply -f ../src/ms_customers/k8s/ms-customers-hpa.yaml
kubectl apply -f ../k8s/deployment.yaml