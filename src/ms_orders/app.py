from flask import Flask, jsonify, request
import mysql.connector
import os
import threading
import grpc
from concurrent import futures
import orders_pb2
import orders_pb2_grpc

app = Flask(__name__)

# Configurações do banco de dados MySQL
dbConfig = {
    'host': os.environ['MYSQL_HOST'],
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': os.environ['MYSQL_DATABASE'],
    'port': 3309
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
def createOrder(orderData):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Inserir nova order
        query = "INSERT INTO orders (order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                
        values = (
            orderData['order_id'],
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
@app.route('/')
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
    orderData = request.json
    if createOrder(orderData):
        return jsonify({'status': 'success', 'message': 'Order created successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to create order'})

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
    def GetAllOrders(self, request, context):
        orders = listAllOrders()
        order_protos = [orders_pb2.Order(
            order_id=order['order_id'],
            customer_id=order['customer_id'],
            order_status=order['order_status'],
            # adicione outros campos conforme necessário
        ) for order in orders]
        return orders_pb2.OrderList(orders=order_protos)

    def CreateOrder(self, request, context):
        createOrder((
            request.order_id,
            request.customer_id,
            request.order_status,
            # adicione outros campos conforme necessário
        ))
        return request

    def UpdateOrderStatus(self, request, context):
        updateOrder(request.order_id, request.new_status)
        return request

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
    app.run(host='0.0.0.0', port=5000)
