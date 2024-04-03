@echo off

rem Constroi imagens Docker para cada serviço
docker-compose -f src\ms_orders\docker-compose.yml build
@REM docker-compose -f src\ms_JESSE_NOME_MICROSERVICO\docker-compose.yml build
@REM docker-compose -f src\ms_JOSE_NOME_MICROSERVICO\docker-compose.yml build

rem Iniciar os containers para cada serviço
docker-compose -f src\ms_orders\docker-compose.yml up -d
@REM docker-compose -f src\ms_JESSE_NOME_MICROSERVICO\docker-compose.yml up -d
@REM docker-compose -f src\ms_JOSE_NOME_MICROSERVICO\docker-compose.yml up -d

rem Aguardar alguns segundos para os containers inicializarem completamente
timeout /t 10 /nobreak >nul

rem Executar migrações de banco de dados (substitua este comando pelo comando real de migração)
python src\ms_orders\utils\parse_dataset.py

echo Building and deployment completed successfully.
