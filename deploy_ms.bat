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
rem Exemplo:
rem docker-compose -f src\ms_orders\docker-compose.yml exec api python manage.py migrate

echo Building and deployment completed successfully.
