import pandas as pd
from sqlalchemy import create_engine
import os

# Defina as credenciais do banco de dados MySQL
MYSQL_HOST = '127.0.0.1'
MYSQL_DATABASE = 'olist_orders'
MYSQL_USER = 'olist_user'
MYSQL_PASSWORD = 'olist_password'

# Crie a conexão com o banco de dados MySQL
engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}')

# Caminho para o arquivo CSV
csv_file = 'D:\WIN_AMBIENTE\Documentos\GitHub\olist-cloud-computing-project\dataset\olist_orders_dataset.csv'



# Carregue os dados do arquivo CSV usando pandas
df = pd.read_csv(csv_file)

# Insira os dados do DataFrame no banco de dados MySQL
df.to_sql('orders', con=engine, if_exists='append', index=False)

print("Dados inseridos com sucesso no banco de dados MySQL.")
