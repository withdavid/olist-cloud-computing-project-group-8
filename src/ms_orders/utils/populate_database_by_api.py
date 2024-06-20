import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Função para enviar dados para a API
def createOrder(orderData):
    api_endpoint = 'http://34.149.123.147/orders'
    payload = {
        "order_id": orderData["order_id"],
        "product_id": orderData["product_id"],
        "customer_id": orderData["customer_id"],
        "order_status": orderData["order_status"],
        "order_purchase_timestamp": orderData["order_purchase_timestamp"],
        "order_approved_at": orderData["order_approved_at"],
        "order_delivered_carrier_date": orderData["order_delivered_carrier_date"],
        "order_delivered_customer_date": orderData["order_delivered_customer_date"],
        "order_estimated_delivery_date": orderData["order_estimated_delivery_date"]
    }
    
    response = requests.post(api_endpoint, json=payload)
    if response.status_code == 200:
        return f"Data for order_id {orderData['order_id']} successfully inserted."
    else:
        return f"Failed to insert data for order_id {orderData['order_id']}. Response code: {response.status_code}"

# CSV do dataset
csv_file = '../dataset/olist_orders_dataset.csv'

# Load CSV file
df = pd.read_csv(csv_file)

# Converte as colunas de datas para o formato YYYY-MM-DD HH:MM
date_columns = [
    'order_purchase_timestamp', 'order_approved_at', 
    'order_delivered_carrier_date', 'order_delivered_customer_date', 
    'order_estimated_delivery_date'
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], format='%d/%m/%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M:%S')

# Verifica se a tabela está vazia (neste caso, apenas verifica se o CSV está vazio)
if not df.empty:
    print("Populating data to API endpoint...")

    # Usar ThreadPoolExecutor para enviar dados em paralelo
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(createOrder, row) for index, row in df.iterrows()]

        for future in as_completed(futures):
            print(future.result())

else:
    print("CSV file is empty. No data insertion required.")
