import requests
import time
import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def conectar_api():
    client = tweepy.Client(access_token=os.environ.get('ACCESS_TOKEN'),
                           access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
                           consumer_key=os.environ.get('CONSUMER_API_KEY'),
                           consumer_secret=os.environ.get('CONSUMER_API_KEY_SECRET'))
    return client

def fazer_requisicao():
    url = os.environ.get('URL_EXCHANGE')
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

def bot():
    hora_inicio = int(os.environ.get('INIT_HOUR'))
    hora_fim = int(os.environ.get('END_HOUR'))
    client = conectar_api()
    while True:
        hora_atual = datetime.now().hour

        if hora_inicio <= hora_atual < hora_fim:
            responseExchange = fazer_requisicao()
            if responseExchange and (float(responseExchange['EURBRL']['pctChange']) > float(os.environ.get('MAX_VARIATION')) or float(responseExchange['EURBRL']['pctChange']) < float(os.environ.get('MIN_VARIATION'))):
                create_tweet(responseExchange, client)
            else:
                print("Não foi possível obter a cotação ou a variação foi menor que o desejado.")
                print("Aguardando 1 minuto antes da próxima requisição...")
            time.sleep(int(os.environ.get('TIME_TO_NEW_REQUEST')))
        else:
            print("Fora do horário de operação. Esperando...")
            time.sleep(int(os.environ.get('TIME_TO_NEW_REQUEST')))

if __name__ == "__main__":
    bot()