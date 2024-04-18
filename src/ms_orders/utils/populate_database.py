import pandas as pd
from sqlalchemy import create_engine, inspect, text

# MYSQL_INFO
MYSQL_HOST = '127.0.0.1'
MYSQL_DATABASE = 'olist_orders'
MYSQL_USER = 'olist_myuser'
MYSQL_PASSWORD = 'olist_password'

# MySQL Conn
engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}')

# Verifica se a tabela orders já existe
inspector = inspect(engine)
if not inspector.has_table('orders'):
    # Se a tabela não existir, carrega a tabela
    with open('./sql/init.sql', 'r') as file:
        sql = file.read()
    engine.execute(sql)

# Cria uma conexão
with engine.connect() as conn:
    # Verifica se a tabela orders está vazia
    result = conn.execute(text('SELECT COUNT(*) FROM orders'))
    if result.scalar() == 0:
        # CSV do dataset
        csv_file = './dataset/olist_orders_dataset.csv'
        
        # Load CSV file
        df = pd.read_csv(csv_file)

        # Insert on DB
        print("Populating data to table orders...")
        df.to_sql('orders', con=engine, if_exists='append', index=False)

        print("Data successfully inserted into MySQL database.")
    else:
        print("Table 'orders' already contains records. No data insertion required.")
