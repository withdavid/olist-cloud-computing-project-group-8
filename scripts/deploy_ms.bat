@echo off

rem Iniciar os containers para cada serviço
docker-compose -f ..\src\ms_orders\docker-compose.yml up -d
docker-compose -f ..\src\ms_customers\docker-compose.yml up -d
docker-compose -f ..\src\ms_products\docker-compose.yml up -d

rem Aguardar alguns segundos para os containers inicializarem completamente
timeout /t 30 /nobreak >nul

echo Building and deployment completed successfully.

@REM kubectl apply -f ..\src/ms_orders/k8s/deployment.yaml
@REM kubectl apply -f ..\src/ms_orders/k8s/ms-orders-hpa.yaml
@REM kubectl apply -f ..\src/ms_products/k8s/deployment.yaml
@REM kubectl apply -f ..\src/ms_products/k8s/ms-products-hpa.yaml
@REM kubectl apply -f ..\src/ms_customers/k8s/deployment.yaml
@REM kubectl apply -f ..\src/ms_customers/k8s/ms-customers-hpa.yaml
@REM kubectl apply -f ..\k8s/deployment.yaml