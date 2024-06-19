import os
import random
import uuid
from datetime import datetime, timedelta
from locust import HttpUser, SequentialTaskSet, task, between

SERVER_IP = os.getenv("SERVER_IP", "http://34.120.159.149")

def random_string(length=6):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(letters) for _ in range(length))

def random_datetime(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

class User(HttpUser):
    wait_time = between(1, 5)

    @task
    class SequenceOfTasks(SequentialTaskSet):
        @task
        def getCustomers(self):
            self.client.get(f"{SERVER_IP}/customers")
        
        @task
        def getCustomerOrders(self):
            self.client.get(f"{SERVER_IP}/customers/12345678/orders")
        
        @task
        def createCustomer(self):
            customer_id = str(random.randint(10000000, 99999999))
            customer_unique_id = str(random.randint(100000, 999999))
            customer_zip_code_prefix = str(random.randint(10000, 99999))
            customer_city = random.choice(["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Porto Alegre", "Curitiba"])
            customer_state = random.choice(["SP", "RJ", "MG", "RS", "PR"])
            self.client.post(
                f"{SERVER_IP}/customers",
                json={
                    "customer_id": customer_id,
                    "customer_unique_id": customer_unique_id,
                    "customer_zip_code_prefix": customer_zip_code_prefix,
                    "customer_city": customer_city,
                    "customer_state": customer_state
                }
            )
        
        @task
        def createProduct(self):
            product_id = str(uuid.uuid4())
            product_category_name = random.choice(["Eletrônicos", "Roupas", "Alimentos", "Livros", "Móveis"])
            product_name_length = random.randint(5, 20)
            product_description_length = random.randint(50, 200)
            product_photos_qty = random.randint(1, 10)
            product_weight_g = random.randint(100, 5000)
            product_length_cm = random.randint(5, 100)
            product_height_cm = random.randint(5, 100)
            product_width_cm = random.randint(5, 100)
            price = round(random.uniform(10.0, 1000.0), 2)
            self.client.post(
                f"{SERVER_IP}/products",
                json={
                    "product_id": product_id,
                    "product_category_name": product_category_name,
                    "product_name_length": product_name_length,
                    "product_description_length": product_description_length,
                    "product_photos_qty": product_photos_qty,
                    "product_weight_g": product_weight_g,
                    "product_length_cm": product_length_cm,
                    "product_height_cm": product_height_cm,
                    "product_width_cm": product_width_cm,
                    "price": price
                }
            )
        
        @task
        def createOrder(self):
            order_id = str(uuid.uuid4())
            product_id = str(uuid.uuid4())
            customer_id = str(random.randint(10000000, 99999999))
            order_status = random.choice(["processing", "shipped", "delivered"])
            now = datetime.now()
            order_purchase_timestamp = now.isoformat()
            order_approved_at = (now + timedelta(minutes=10)).isoformat()
            order_delivered_carrier_date = (now + timedelta(days=1)).isoformat()
            order_delivered_customer_date = (now + timedelta(days=5)).isoformat()
            order_estimated_delivery_date = (now + timedelta(days=10)).isoformat()
            self.client.post(
                f"{SERVER_IP}/orders",
                json={
                    "order_id": order_id,
                    "product_id": product_id,
                    "customer_id": customer_id,
                    "order_status": order_status,
                    "order_purchase_timestamp": order_purchase_timestamp,
                    "order_approved_at": order_approved_at,
                    "order_delivered_carrier_date": order_delivered_carrier_date,
                    "order_delivered_customer_date": order_delivered_customer_date,
                    "order_estimated_delivery_date": order_estimated_delivery_date
                }
            )
        
        @task
        def updateCustomer(self):
            self.client.put(
                f"{SERVER_IP}/customers/12345678",
                json={
                    "customer_unique_id": "789012",
                    "customer_zip_code_prefix": "54321",
                    "customer_city": "Rio de Janeiro",
                    "customer_state": "RJ"
                }
            )
        
        @task
        def getProducts(self):
            self.client.get(f"{SERVER_IP}/products")
        
        @task
        def updateProduct(self):
            self.client.put(
                f"{SERVER_IP}/products/123",
                json={
                    "product_category_name": "Eletrônicos",
                    "product_name_length": 20,
                    "product_description_length": 150,
                    "product_photos_qty": 3,
                    "product_weight_g": 1200,
                    "product_length_cm": 25,
                    "product_height_cm": 10,
                    "product_width_cm": 15,
                    "price": 9.99
                }
            )
        
        @task
        def getOrders(self):
            self.client.get(f"{SERVER_IP}/orders")
        
        @task
        def updateOrder(self):
            self.client.put(
                f"{SERVER_IP}/orders/AAA10242fe8c5a6d12222dd792cb16214",
                json={
                    "order_status": "delivered",
                    "order_purchase_timestamp": "2024-05-15 16:04:47",
                    "order_approved_at": "2024-05-15 16:04:47",
                    "order_delivered_carrier_date": "2024-05-16 16:04:47",
                    "order_delivered_customer_date": "2024-05-17 16:04:47",
                    "order_estimated_delivery_date": "2024-05-18 16:04:47"
                }
            )

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
