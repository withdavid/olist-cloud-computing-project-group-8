@echo off

rem Constroi imagens Docker para cada serviço
docker-compose -f src\ms_orders\docker-compose.yml build
docker-compose -f src\ms_customers\docker-compose.yml build
docker-compose -f src\ms_products\docker-compose.yml build

rem Iniciar os containers para cada serviço
docker-compose -f src\ms_orders\docker-compose.yml up -d
docker-compose -f src\ms_customers\docker-compose.yml up -d
docker-compose -f src\ms_products\docker-compose.yml up -d

rem Aguardar alguns segundos para os containers inicializarem completamente
timeout /t 30 /nobreak >nul

rem Executar migrações de banco de dados (substitua este comando pelo comando real de migração)
python src\ms_orders\utils\parse_dataset.py
python src\ms_customers\utils\parse_dataset.py
python src\ms_products\utils\parse_dataset.py

echo Building and deployment completed successfully.
