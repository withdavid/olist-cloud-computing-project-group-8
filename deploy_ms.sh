#!/bin/bash

# Constroi imagens Docker para cada serviço
docker-compose -f src/ms_order/docker-compose.yml build
# docker-compose -f src/ms_JESSE_NOME_MICROSERVICO/docker-compose.yml build
# docker-compose -f src/ms_JOSE_NOME_MICROSERVICO/docker-compose.yml build

# Iniciar os containers para cada serviço
docker-compose -f src/ms_order/docker-compose.yml up -d
# docker-compose -f src/ms_JESSE_NOME_MICROSERVICO/docker-compose.yml up -d
# docker-compose -f src/ms_JOSE_NOME_MICROSERVICO/docker-compose.yml up -d

# Aguardar alguns segundos para os containers inicializarem completamente
sleep 10

# Executar migrações de banco de dados (substitua este comando pelo comando real de migração)
# Exemplo:
# docker-compose -f src/ms_order/docker-compose.yml exec api python manage.py migrate

echo "Building and deployment completed successfully."