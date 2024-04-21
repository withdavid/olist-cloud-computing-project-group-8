# Use a imagem oficial do Python
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho do contêiner
COPY requirements.txt /app
COPY app.py /app

# Instala as dependências Python especificadas no arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta em que a aplicação estará em execução
EXPOSE 5001

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
