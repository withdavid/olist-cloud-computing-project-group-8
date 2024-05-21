from flask import Flask, jsonify, request
import mysql.connector
import os
import threading
import grpc
from concurrent import futures
from orders_pb2 import( 
    CustomerOrder,
    CustomerResponse
)
import orders_pb2_grpc
from customers_cliente import CustomerClient
from google.protobuf.json_format import MessageToDict

# import google.oauth2 

app = Flask(__name__)


customer_svc = CustomerClient()


# Configurações do banco de dados MySQL
dbConfig = {
    'host': os.environ['MYSQL_HOST'],
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': os.environ['MYSQL_DATABASE'],
    'port': 3309
}

# API KEY: AIzaSyBNpbxlyujXXCcyxKNK64Wk3mbqlCWQx3w


# Função para verificar a chave de API
# def verify_api_key(api_key):
#     try:
#         # Carrega a chave de API do arquivo JSON
#         creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        
#         # Verifica se a chave de API é válida
#         if api_key == creds.token:
#             return True
#         else:
#             return False
#     except Exception as e:
#         return False

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


# Função para listar todas as orders
def listAllOrders():
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor(dictionary=True)

        # Consulta para obter todas as orders
        query = "SELECT * FROM orders"
        cursor.execute(query)
        orders = cursor.fetchall()

        cursor.close()
        connection.close()

        return orders
    except Exception as e:
        return None
    
    # Função para listar todas as orders do cliente
def listClienteOrders(clienteId):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor(dictionary=True)
        print("Chegou aqui ")
        # Consulta para obter todas as orders
        query = "SELECT customer_id, order_id, order_status, order_delivered_customer_date FROM orders WHERE customer_id = %s"
        cursor.execute(query, (clienteId,))
        orders = cursor.fetchall()

        cursor.close()
        connection.close()

        return orders
    except Exception as e:
        return None
def createOrder(orderData):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Inserir nova order
        query = "INSERT INTO orders (order_id, product_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                
        values = (
            orderData['order_id'],
            orderData['product_id'],
            orderData['customer_id'],
            orderData['order_status'],
            orderData['order_purchase_timestamp'],
            orderData['order_approved_at'],
            orderData['order_delivered_carrier_date'],
            orderData['order_delivered_customer_date'],
            orderData['order_estimated_delivery_date']
            )
        
        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        return False

# Função para atualizar uma order
def updateOrder(orderId, orderData):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Atualizar status da order
        query = "UPDATE orders SET order_status = %s, order_purchase_timestamp = %s, order_approved_at = %s, order_delivered_carrier_date = %s, order_delivered_customer_date = %s, order_estimated_delivery_date = %s WHERE order_id = %s"
        
        values = (
            orderData['order_status'],
            orderData['order_purchase_timestamp'],
            orderData['order_approved_at'],
            orderData['order_delivered_carrier_date'],
            orderData['order_delivered_customer_date'],
            orderData['order_estimated_delivery_date'],
            orderId
            )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print(e)
        return False


# Função para eliminar todas as orders
def deleteAllOrders():
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Elimina todas as orders
        query = "DELETE FROM orders"
        cursor.execute(query)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        return False

# Rota para testar a conexão com o banco de dados
@app.route('/orders/health')
def heartbeat():
    result = testDbConnection()
    if result['status'] == 'operational':
        return jsonify({'status': 'operational', 'message': 'Database connection operational'})
    else:
        return jsonify({'status': 'error', 'message': 'Database connection error'})

# Rota para listar todas as ordens
@app.route('/orders', methods=['GET'])
def getAllOrders():
    orders = listAllOrders()
    if orders is not None:
        return jsonify({'status': 'success', 'orders': orders})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to retrieve orders'})

# Rota para criar uma nova order
@app.route('/orders', methods=['POST'])
def createNewOrder():
    # api_key = request.headers.get('X-API-Key')
    # if not api_key:
    #     return jsonify({'error': 'API key missing'}), 401
    
    # if verify_api_key(api_key):
    #     # Se a chave de API for válida
    orderData = request.json

    #Requisição ao serviço Customer via grpc
    exists = customer_svc.IsCustomer(orderData['customer_id'])
    exists = MessageToDict(exists)
    print(f'{exists}')
    if exists['msg'] == "true":
        if createOrder(orderData):
            return jsonify({'status': 'success', 'message': 'Order created successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to create order'})
    else:   return jsonify({'status': 'error', 'message': 'Invalid Custumer'})
    


# Rota para atualizar uma order
@app.route('/orders/<string:orderId>', methods=['PUT'])
def updateExistingOrder(orderId):
    orderData = request.json
    if updateOrder(orderId, orderData):
        return jsonify({'status': 'success', 'message': 'Order updated successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to update order'})

# Rota para eliminar todas as orders
@app.route('/orders', methods=['DELETE'])
def deleteAllExistingOrders():
    if deleteAllOrders():
        return jsonify({'status': 'success', 'message': 'All orders deleted successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to delete all orders'})



# Implementação do serviço gRPC
class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def GetCustomerInfo(self, request, context):
        try:
            print(f"Chegou aqui: {request.customer_id}")
            clienteId = request.customer_id
            orders = listClienteOrders(clienteId)
            if orders is None:
                order_protos = []
            else:
                order_protos = [
                        CustomerOrder(
                            customer_id=order['customer_id'],
                            order_id=order['order_id'],
                            order_status=order['order_status'],
                            order_delivered_customer_date=order['order_delivered_customer_date'].strftime('%Y-%m-%d %H:%M:%S')
                        ) for order in orders
                    ]

            return CustomerResponse(costumers_orders=order_protos)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
            return CustomerResponse()
    
# Função para iniciar o servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    server.wait_for_termination()

# Iniciar o servidor gRPC em uma thread separada
if __name__ == '__main__':
    grpc_server_thread = threading.Thread(target=serve)
    grpc_server_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
