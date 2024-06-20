import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Função para enviar dados para a API
def createProduct(productData):
    api_endpoint = 'http://34.149.123.147/products'
    payload = {
        "product_id": productData["product_id"],
        "product_category_name": productData["product_category_name"],
        "product_name_length": productData["product_name_length"],
        "product_description_length": productData["product_description_length"],
        "product_photos_qty": productData["product_photos_qty"],
        "product_weight_g": productData["product_weight_g"],
        "product_length_cm": productData["product_length_cm"],
        "product_height_cm": productData["product_height_cm"],
        "product_width_cm": productData["product_width_cm"],
        "price": productData["price"]
    }
    
    response = requests.post(api_endpoint, json=payload)
    if response.status_code == 200:
        return f"Data for product_id {productData['product_id']} successfully inserted."
    else:
        return f"Failed to insert data for product_id {productData['product_id']}. Response code: {response.status_code}"

# CSV do dataset
csv_file = '../dataset/olist_products_dataset.csv'

# Load CSV file
df = pd.read_csv(csv_file)

# Verifica se a tabela está vazia (neste caso, apenas verifica se o CSV está vazio)
if not df.empty:
    print("Populating data to API endpoint...")

    # Usar ThreadPoolExecutor para enviar dados em paralelo
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(createProduct, row) for index, row in df.iterrows()]

        for future in as_completed(futures):
            print(future.result())

else:
    print("CSV file is empty. No data insertion required.")
