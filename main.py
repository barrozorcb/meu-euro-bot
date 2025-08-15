import requests
import time
import tweepy
import config
from datetime import datetime

def conectar_api():
    client = tweepy.Client(access_token=config.access_token,
                           access_token_secret=config.access_token_secret,
                           consumer_key=config.consumer_api_key,
                           consumer_secret=config.consumer_api_key_secret)
    return client

# Função para realizar a requisição à API
def fazer_requisicao():
    url = config.url_exchange
    try:
        exchangeResponse = requests.get(url)
        if exchangeResponse.status_code == 200:
            print("Requisição bem-sucedida!")
            print(exchangeResponse.json())
            return exchangeResponse.json()
        else:
            print(f"Erro ao fazer a requisição: {exchangeResponse.status_code}")
    except Exception as e:
        print(f"Erro ao tentar se conectar à API: {e}")

def create_tweet(exchangeResponse, client):
    texto = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f"\n Cotação EUR/BRL:\nCompra: {exchangeResponse['EURBRL']['bid']}, Venda: {exchangeResponse['EURBRL']['ask']}\nVariação: {exchangeResponse['EURBRL']['pctChange']}%"
    client.create_tweet(text=texto, user_auth=True)
    print("Tweet enviado com sucesso!")

# Função principal do bot
def bot():
    hora_inicio = config.init_hour  # Início: 09:00
    hora_fim = config.end_hour  # Fim: 17:00
    client = conectar_api()
    while True:
        # Verificar se a hora atual está dentro do intervalo desejado
        hora_atual = datetime.now().hour

        if hora_inicio <= hora_atual < hora_fim:
            responseExchange = fazer_requisicao()  # Realiza a requisição à API
            if responseExchange and (float(responseExchange['EURBRL']['pctChange']) > config.max_variation or float(responseExchange['EURBRL']['pctChange']) < config.min_variation):
                create_tweet(responseExchange, client)
            else:
                print("Não foi possível obter a cotação ou a variação foi menor que o desejado.")
                print("Aguardando 1 minuto antes da próxima requisição...")
            time.sleep(config.time_to_new_request)  # Espera 1 minuto (60 segundos)
        else:
            print("Fora do horário de operação. Esperando...")
            time.sleep(config.time_to_new_request)  # Espera 1 minuto (60 segundos)

if __name__ == "__main__":
    bot()