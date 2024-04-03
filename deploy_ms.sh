#!/bin/bash

# Constroi imagens Docker para cada serviço
docker-compose -f src/ms_orders/docker-compose.yml build
docker-compose -f src/ms_products/docker-compose.yml build
docker-compose -f src/ms_customers/docker-compose.yml build

# Iniciar os containers para cada serviço
docker-compose -f src/ms_orders/docker-compose.yml up -d
docker-compose -f src/ms_products/docker-compose.yml up -d
docker-compose -f src/ms_customers/docker-compose.yml up -d

# Aguardar alguns segundos para os containers inicializarem completamente
sleep 10

# Executar migrações de banco de dados (substitua este comando pelo comando real de migração)
python src\ms_orders\utils\parse_dataset.py

echo "Building and deployment completed successfully."