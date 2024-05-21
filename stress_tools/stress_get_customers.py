import requests
import time
import threading

# URL do endpoint
url = 'http://34.111.24.184/customers'

def send_request():
    while True:
        try:
            # Envia a requisição GET
            response = requests.get(url)
            
            # Verifica se a requisição foi bem sucedida (status code 200)
            # if response.status_code == 200:
            #     # Processa a resposta (opcional: você pode adicionar qualquer lógica de processamento aqui)
            #     print(f"Resposta recebida: {response.json()}")
            # else:
            #     print(f"Erro ao acessar o endpoint: Status Code {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            # Captura qualquer exceção que ocorrer durante a requisição
            print(f"Ocorreu um erro ao fazer a requisição: {e}")

# Número de threads
num_threads = 1000

# Criar e iniciar múltiplas threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=send_request)
    thread.start()
    threads.append(thread)

# Aguardar todas as threads terminarem (nesse caso, nunca termina porque o loop é infinito)
for thread in threads:
    thread.join()
