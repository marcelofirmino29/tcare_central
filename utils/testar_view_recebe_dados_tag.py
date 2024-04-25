# import requests

# # URL da sua view
# url = 'http://127.0.0.1:8000/api/ble/'  # Substitua pela URL correta

# # Dados a serem enviados (simulando dados do Raspberry Pi)
# data = {
#     'device_id': 'raspberry_pi_001',
#     'rssi': '-60'  # Exemplo de valor de RSSI
# }

# try:
#     # Fazendo a requisição POST
#     response = requests.post(url, data=data)

#     # Verifica se a requisição foi bem-sucedida (código 200)
#     if response.status_code == 200:
#         print('Requisição bem-sucedida!')
#         print(response.json())  # Imprime a resposta da view
#     else:
#         print('Erro ao enviar requisição:', response.status_code)

# except requests.exceptions.RequestException as e:
#     print('Erro de requisição:', e)



import requests
from datetime import datetime

def testa_recebe_dados_tag():
    url = 'http://127.0.0.1:8000/api/ble/'  # Substitua pela URL correta da sua view
    a=0
    while a < 10:
        # Dados simulados a serem enviados na requisição POST
        data = {
            'mac_tag': 'bc:57:29:00:a0:0a'.replace(':', '').upper(),  # Exemplo de endereço MAC da tag BLE
            'rssi': '-70',  # Exemplo de valor RSSI (convertido para string)
            'mac_raspberry': 'e6:9a:69:a7:9c:72'.replace(':', '').upper(),  # Exemplo de endereço MAC do Raspberry Pi
            'data_leitura': datetime.now().isoformat
        }

        try:
            response = requests.post(url, data=data)

            if response.status_code == 200:
                print("Requisição bem-sucedida!")
                print("Resposta do servidor:", response.json())
            else:
                print("Erro na requisição. Código de status:", response.status_code)
                print("Resposta do servidor:", response.text)
        except Exception as e:
            print("Erro ao enviar requisição:", e)
        a = a+1

if __name__ == '__main__':
    testa_recebe_dados_tag()
