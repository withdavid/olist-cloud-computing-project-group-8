import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Função para enviar dados para a API
def send_data(row):
    api_endpoint = 'http://34.149.123.147/customers'
    payload = {
        "customer_id": row["customer_id"],
        "customer_unique_id": row["customer_unique_id"],
        "customer_zip_code_prefix": row["customer_zip_code_prefix"],
        "customer_city": row["customer_city"],
        "customer_state": row["customer_state"]
    }
    
    response = requests.post(api_endpoint, json=payload)
    if response.status_code == 200:
        return f"Data for customer_id {row['customer_id']} successfully inserted."
    else:
        return f"Failed to insert data for customer_id {row['customer_id']}. Response code: {response.status_code}"

# CSV do dataset
csv_file = '../dataset/olist_customers_dataset.csv'

# Load CSV file
df = pd.read_csv(csv_file)

# Verifica se a tabela está vazia (neste caso, apenas verifica se o CSV está vazio)
if not df.empty:
    print("Populating data to API endpoint...")

    # Usar ThreadPoolExecutor para enviar dados em paralelo
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_data, row) for index, row in df.iterrows()]

        for future in as_completed(futures):
            print(future.result())

else:
    print("CSV file is empty. No data insertion required.")
