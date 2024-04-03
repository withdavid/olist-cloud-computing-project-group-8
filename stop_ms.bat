@echo off

rem Parar os containers Docker para cada serviço
docker-compose -f src\ms_orders\docker-compose.yml down
docker-compose -f src\ms_products\docker-compose.yml down
docker-compose -f src\ms_customers\docker-compose.yml down

echo Docker containers stopped successfully.
