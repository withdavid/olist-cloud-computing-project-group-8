from flask import Flask, jsonify, request
import mysql.connector
import os
from decouple import config

app = Flask(__name__)

# Configurações do banco de dados MySQL
dbConfig = {
    'host': config('MYSQL_HOST'),
    'user': config('MYSQL_USER'),
    'password': config('MYSQL_PASSWORD'),
    'database': config('MYSQL_DATABASE'),
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
