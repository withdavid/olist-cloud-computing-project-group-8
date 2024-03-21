from flask import Flask, jsonify
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

# Rota para testar a conexão com o banco de dados
@app.route('/')
def heartbeat():
    result = test_db_connection()
    if result['status'] == 'operational':
        return jsonify({'status': 'operational', 'message': 'Database connection operational'})
    else:
        return jsonify({'status': 'error', 'message': 'Database connection error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
