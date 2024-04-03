#!/bin/bash

# Parar os containers Docker para cada serviço
docker-compose -f src/ms_orders/docker-compose.yml down
#@REM docker-compose -f src/ms_JESSE_NOME_MICROSERVICO/docker-compose.yml down
#@REM docker-compose -f src/ms_JOSE_NOME_MICROSERVICO/docker-compose.yml down

echo Docker containers stopped successfully.
