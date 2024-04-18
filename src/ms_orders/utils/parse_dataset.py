import pandas as pd
from sqlalchemy import create_engine, inspect

# MYSQL_INFO
MYSQL_HOST = '127.0.0.1'
MYSQL_DATABASE = 'olist_orders'
MYSQL_USER = 'olist_myuser'
MYSQL_PASSWORD = 'olist_password'

# MySQL Conn
engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}')

# CSV do dataset
csv_file = '../../../dataset/olist_orders_dataset.csv'

# Verifica se a tabela orders ja existe
inspector = inspect(engine)
if not inspector.has_table('orders'):
    # Se a tabela não existir, carrega a tabela
    with open('./sql/orders.sql', 'r') as file:
        sql = file.read()
    engine.execute(sql)

# Load CSV file
df = pd.read_csv(csv_file)

# Insert on DB
df.to_sql('orders', con=engine, if_exists='append', index=False)

print("Data successfully inserted into MySQL database.")