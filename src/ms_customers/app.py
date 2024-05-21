from flask import Flask, jsonify, request
import mysql.connector
import os
import threading
import grpc
from concurrent import futures
from customers_pb2 import(CustomerRequest, CustomerResponse)
import customers_pb2_grpc
from google.protobuf.json_format import MessageToDict
from orders_cliente import OrdersClient

app = Flask(__name__)

orders_svc = OrdersClient()

# Configurações do banco de dados MySQL
dbConfig = {
    'host': os.environ['MYSQL_HOST'],
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': os.environ['MYSQL_DATABASE'],
    'port': 3307
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


# Função para listar todos os clientes
def listAllCustomers():
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor(dictionary=True)

        # Consulta para obter todos os clientes
        query = "SELECT * FROM customers"
        cursor.execute(query)
        customers = cursor.fetchall()

        cursor.close()
        connection.close()

        return customers
    except Exception as e:
        return None

# Função para listar todos os clientes
def customerExist(customerId):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor(dictionary=True)

        # Consulta para obter todos os clientes
        query = "SELECT * FROM customers where customer_id = %s"
        cursor.execute(query, (customerId,))
        customers = cursor.fetchall()

        cursor.close()
        connection.close()

        # Verificar se a consulta retornou dados
        if customers:
            return True  # A consulta retornou dados
        else:
            return False  # A consulta não retornou dados
    except Exception as e:
        return None

# Função para criar um novo cliente
def createCustomer(customerData):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Inserir novo cliente
        query = "INSERT INTO customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state) VALUES (%s, %s, %s, %s, %s)"
        
        values = (
            customerData['customer_id'],
            customerData['customer_unique_id'],
            customerData['customer_zip_code_prefix'],
            customerData['customer_city'],
            customerData['customer_state']
            )
        
        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        return False

# Função para atualizar os dados de um cliente
def updateCustomerData(customer_id, customerData):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Atualizar os dados do cliente
        query = "UPDATE customers SET customer_unique_id = %s, customer_zip_code_prefix = %s, customer_city = %s, customer_state = %s WHERE customer_id = %s"
        
        values = (
            customerData['customer_unique_id'],
            customerData['customer_zip_code_prefix'],
            customerData['customer_city'],
            customerData['customer_state'],
            customer_id
            )
        
        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print(e)
        return False

# Função para eliminar todos os clientes
def deleteAllCustomers():
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Elimina todos os clientes
        query = "DELETE FROM customers"
        cursor.execute(query)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        return False

# Rota para testar a conexão com o banco de dados
@app.route('/customers/health')
def heartbeat():
    result = testDbConnection()
    if result['status'] == 'operational':
        return jsonify({'status': 'operational', 'message': 'Database connection operational'})
    else:
        return jsonify({'status': 'error', 'message': 'Database connection error'})

# Rota para listar todos os clientes
@app.route('/customers/<string:clienteId>/orders', methods=['GET'])
def getCustomersOrders(clienteId):
    customers = orders_svc.getUserOrders(clienteId)

    if customers is not None:
        # Converta o objeto protobuf para um dicionário
        result = MessageToDict(customers)
        return jsonify({'status': 'success', 'customers': result})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to retrieve customers orders'})
    
# Rota para listar todos os clientes
@app.route('/customers', methods=['GET'])
def getAllCustomers():
    customers = listAllCustomers()
    if customers is not None:
        return jsonify({'status': 'success', 'customers': customers})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to retrieve customers'})

# Rota para criar um novo cliente
@app.route('/customers', methods=['POST'])
def createNewCustomer():
    customerData = request.json
    if createCustomer(customerData):
        return jsonify({'status': 'success', 'message': 'Customer created successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to create customer'})
    
# Rota para atualizar um cliente
@app.route('/customers/<string:customer_id>', methods=['PUT'])
def updateCustomer(customer_id):
    customerData = request.json
    if updateCustomerData(customer_id, customerData):
        return jsonify({'status': 'success', 'message': 'Customer data updated successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to update customer data'})

# Rota para eliminar todos os clientes
@app.route('/customers', methods=['DELETE'])
def deleteAllExistingCustomers():
    if deleteAllCustomers():
        return jsonify({'status': 'success', 'message': 'All customers deleted successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to delete all customers'})


# Integração do gRPC
class CustomerService(customers_pb2_grpc.CustomerServiceServicer):
    def IsCustomer(self, request, context):
        customers = customerExist(request.customer_id)

        if customers:
         return CustomerResponse(msg="true")
        
        return CustomerResponse(msg="false")

# Integração do gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customers_pb2_grpc.add_CustomerServiceServicer_to_server(CustomerService(), server)
    server.add_insecure_port('[::]:50051')  # Use uma porta diferente para cada microserviço
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    grpc_server_thread = threading.Thread(target=serve)
    grpc_server_thread.start()
    app.run(host='0.0.0.0', port=5000)
