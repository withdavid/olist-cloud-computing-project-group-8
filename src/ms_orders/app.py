from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# Configurações do banco de dados MySQL
db_config = {
    'host': os.environ['MYSQL_HOST'],
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': os.environ['MYSQL_DATABASE']
}

# Função para testar a conexão com o banco de dados
def test_db_connection():
    try:
        # Conecta ao banco de dados
        connection = mysql.connector.connect(**db_config)
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

# Função para listar as ordens de um usuário
def list_user_orders(user_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Consulta para obter as ordens do usuário
        query = "SELECT * FROM orders WHERE customer_id = %s"
        cursor.execute(query, (user_id,))
        orders = cursor.fetchall()

        cursor.close()
        connection.close()

        return orders
    except Exception as e:
        return None

# Rota para testar a conexão com o banco de dados
@app.route('/')
def heartbeat():
    result = test_db_connection()
    if result['status'] == 'operational':
        return jsonify({'status': 'operational', 'message': 'Database connection operational'})
    else:
        return jsonify({'status': 'error', 'message': 'Database connection error'})

# Rota para listar todas as ordens de um usuário
@app.route('/listorders/<string:user_id>', methods=['POST'])
def list_orders_by_user(user_id):
    orders = list_user_orders(user_id)
    if orders is not None:
        return jsonify({'status': 'success', 'orders': orders})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to retrieve user orders'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
