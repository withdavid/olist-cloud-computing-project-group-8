# Use a imagem oficial do Python
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho do contêiner
COPY requirements.txt /app
COPY .env /app
COPY app.py /app
COPY customers_pb2.py /app
COPY customers_pb2_grpc.py /app
COPY orders_cliente.py /app
COPY orders_pb2_grpc.py /app
COPY orders_pb2.py /app

# Instala as dependências Python especificadas no arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta em que a aplicação estará em execução
EXPOSE 5001 50051

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
