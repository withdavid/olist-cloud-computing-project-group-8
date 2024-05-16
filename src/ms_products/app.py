from flask import Flask, jsonify, request
import mysql.connector
import os
import threading
import grpc
from concurrent import futures
import products_pb2
import products_pb2_grpc

app = Flask(__name__)

# Configurações do banco de dados MySQL
dbConfig = {
    'host': os.environ['MYSQL_HOST'],
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': os.environ['MYSQL_DATABASE'],
    'port': 3308  # Porta MySQL ajustada para 3308
}

# Função para testar a conexão com o banco de dados
def testDbConnection():
    try:
        # Conecta ao banco de dados
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Executa uma consulta
        cursor.execute("SELECT 'ok!'")

        # Obtém o resultado
        result = cursor.fetchone()

        # Fecha a conexão
        cursor.close()
        connection.close()

        return {'status': 'operational', 'message': result[0]}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Função para listar todos os produtos
def listAllProducts():
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor(dictionary=True)

        # Consulta para obter todos os produtos
        query = "SELECT * FROM products"
        cursor.execute(query)
        products = cursor.fetchall()

        cursor.close()
        connection.close()

        return products
    except Exception as e:
        return None

# Função para criar um novo produto
def createProduct(productData):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Inserir novo produto
        query = "INSERT INTO products (product_id, product_category_name, product_name_length, product_description_length, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                
        values = (
            productData['product_id'],
            productData['product_category_name'],
            productData['product_name_length'],
            productData['product_description_length'],
            productData['product_photos_qty'],
            productData['product_weight_g'],
            productData['product_length_cm'],
            productData['product_height_cm'],
            productData['product_width_cm']
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print(e)
        return False

# Função para atualizar um produto
def updateProduct(productId, newProductData):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Atualizar o produto
        query = "UPDATE products SET product_category_name = %s, product_name_length = %s, product_description_length = %s, product_photos_qty = %s, product_weight_g = %s, product_length_cm = %s, product_height_cm = %s, product_width_cm = %s WHERE product_id = %s"
                
        values = (
            newProductData['product_category_name'],
            newProductData['product_name_length'],
            newProductData['product_description_length'],
            newProductData['product_photos_qty'],
            newProductData['product_weight_g'],
            newProductData['product_length_cm'],
            newProductData['product_height_cm'],
            newProductData['product_width_cm'],
            productId
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print(e)
        return False


# Função para eliminar todos os produtos
def deleteAllProducts():
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Elimina todos os produtos
        query = "DELETE FROM products"
        cursor.execute(query)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        return False

# Implementação dos métodos do serviço gRPC
class ProductService(products_pb2_grpc.ProductServiceServicer):
    def GetAllProducts(self, request, context):
        products = listAllProducts()
        product_protos = [products_pb2.Product(
            product_id=product['product_id'],
            product_category_name=product['product_category_name'],
            product_name_length=product['product_name_length'],
            product_description_length=product['product_description_length'],
            product_photos_qty=product['product_photos_qty'],
            product_weight_g=product['product_weight_g'],
            product_lenght_cm=product['product_lenght_cm'],
            product_height_cm=product['product_height_cm'],
            product_width_cm=product['product_width_cm']
        ) for product in products]
        return products_pb2.ProductList(products=product_protos)

    def CreateProduct(self, request, context):
        createProduct((
            request.product_id,
            request.product_category_name,
            request.product_name_length,
            request.product_description_length,
            request.product_photos_qty,
            request.product_weight_g,
            request.product_lenght_cm,
            request.product_height_cm,
            request.product_width_cm
        ))
        return request

    def UpdateProduct(self, request, context):
        updateProduct(request.product_id, (
            request.product_category_name,
            request.product_name_length,
            request.product_description_length,
            request.product_photos_qty,
            request.product_weight_g,
            request.product_lenght_cm,
            request.product_height_cm,
            request.product_width_cm
        ))
        return request

# Inicialização do servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    products_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port('[::]:50052')  # Porta gRPC ajustada para 50052
    server.start()
    server.wait_for_termination()

# Rota para testar a conexão com o banco de dados
@app.route('/')
def heartbeat():
    result = testDbConnection()
    if result['status'] == 'operational':
        return jsonify({'status': 'operational', 'message': 'Database connection operational'})
    else:
        return jsonify({'status': 'error', 'message': 'Database connection error'})

# Rota para listar todos os produtos (para uso interno, não para chamadas gRPC)
@app.route('/products', methods=['GET'])
def getAllProducts():
    products = listAllProducts()
    if products is not None:
        return jsonify({'status': 'success', 'products': products})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to retrieve products'})

# Rota para criar um novo produto (para uso interno, não para chamadas gRPC)
@app.route('/products', methods=['POST'])
def createNewProduct():
    productData = request.json
    if createProduct(productData):
        return jsonify({'status': 'success', 'message': 'Product created successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to create product'})

# Rota para atualizar um produto (para uso interno, não para chamadas gRPC)
@app.route('/products/<string:productId>', methods=['PUT'])
def updateExistingProduct(productId):
    newProductData = request.json
    if updateProduct(productId, newProductData):
        return jsonify({'status': 'success', 'message': 'Product updated successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to update product'})

# Rota para eliminar todos os produtos (para uso interno, não para chamadas gRPC)
@app.route('/products', methods=['DELETE'])
def deleteAllExistingProducts():
    if deleteAllProducts():
        return jsonify({'status': 'success', 'message': 'All products deleted successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to delete all products'})

if __name__ == '__main__':
    grpc_server_thread = threading.Thread(target=serve)
    grpc_server_thread.start()
    app.run(host='0.0.0.0', port=5000)
