from flask import Flask, jsonify, request
import mysql.connector
import os

import grpc
from concurrent import futures
import customer_pb2
import customer_pb2_grpc

app = Flask(__name__)

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

# Integração do gRPC
class CustomerService(customer_pb2_grpc.CustomerServiceServicer):
    def GetAllCustomers(self, request, context):
        customers = listAllCustomers()
        customer_protos = [customer_pb2.Customer(
            customer_id=customer['customer_id'],
            customer_unique_id=customer['customer_unique_id'],
            customer_zip_code_prefix=customer['customer_zip_code_prefix'],
            customer_city=customer['customer_city'],
            customer_state=customer['customer_state']
        ) for customer in customers]
        return customer_pb2.CustomerList(customers=customer_protos)

    def CreateCustomer(self, request, context):
        customer_data = (
            request.customer_id,
            request.customer_unique_id,
            request.customer_zip_code_prefix,
            request.customer_city,
            request.customer_state
        )
        if createCustomer(customer_data):
            return request
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to create customer")

    def DeleteAllCustomers(self, request, context):
        if deleteAllCustomers():
            return customer_pb2.Empty()
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to delete all customers")

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

# Função para criar um novo cliente
def createCustomer(customerData):
    try:
        connection = mysql.connector.connect(**dbConfig)
        cursor = connection.cursor()

        # Inserir novo cliente
        query = "INSERT INTO customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, customerData)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
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
@app.route('/')
def heartbeat():
    result = testDbConnection()
    if result['status'] == 'operational':
        return jsonify({'status': 'operational', 'message': 'Database connection operational'})
    else:
        return jsonify({'status': 'error', 'message': 'Database connection error'})

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

# Rota para eliminar todos os clientes
@app.route('/customers', methods=['DELETE'])
def deleteAllExistingCustomers():
    if deleteAllCustomers():
        return jsonify({'status': 'success', 'message': 'All customers deleted successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to delete all customers'})


# Integração do gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customer_pb2_grpc.add_CustomerServiceServicer_to_server(CustomerService(), server)
    server.add_insecure_port('[::]:50052')  # Use uma porta diferente para cada microserviço
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    app.run(host='0.0.0.0', port=5000)
