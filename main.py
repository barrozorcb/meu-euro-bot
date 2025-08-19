import requests # type: ignore
import time
import tweepy # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from datetime import datetime

load_dotenv()


def conectar_api():
    client = tweepy.Client(access_token=os.environ.get('ACCESS_TOKEN'),
                           access_token_secret=os.environ.get(
                               'ACCESS_TOKEN_SECRET'),
                           consumer_key=os.environ.get('CONSUMER_API_KEY'),
                           consumer_secret=os.environ.get('CONSUMER_API_KEY_SECRET'))
    return client


def fazer_requisicao():
    url = os.environ.get('URL_EXCHANGE')
    if not url:
        print("Erro: a variável de ambiente 'URL_EXCHANGE' não está definida.")
        return None
    try:
        exchangeResponse = requests.get(url)
        if exchangeResponse.status_code == 200:
            print("Requisição bem-sucedida!")
            print(exchangeResponse.json())
            return exchangeResponse.json()
        else:
            print(
                f"Erro ao fazer a requisição: {exchangeResponse.status_code}")
    except Exception as e:
        print(f"Erro ao tentar se conectar à API: {e}")


def create_tweet(exchangeResponse, client):
    texto = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + \
        f"\n Cotação EUR/BRL:\nCompra: R$ {float(exchangeResponse['EURBRL']['bid']):.2f}, Venda: R$ {float(exchangeResponse['EURBRL']['ask']):.2f}\nVariação: {float(exchangeResponse['EURBRL']['pctChange']):.3f}%"
    client.create_tweet(text=texto, user_auth=True)
    print("Tweet enviado com sucesso!")


def bot():
    init_hour_str = os.environ.get('INIT_HOUR')
    end_hour_str = os.environ.get('END_HOUR')
    if init_hour_str is None or end_hour_str is None:
        raise ValueError("As variáveis de ambiente 'INIT_HOUR' e/ou 'END_HOUR' não estão definidas.")
    hora_inicio = int(init_hour_str)
    hora_fim = int(end_hour_str)
    client = conectar_api()
    max_variation_str = os.environ.get('MAX_VARIATION')
    min_variation_str = os.environ.get('MIN_VARIATION')
    time_to_new_request_str = os.environ.get('TIME_TO_NEW_REQUEST')

    if max_variation_str is None or min_variation_str is None or time_to_new_request_str is None:
        raise ValueError("As variáveis de ambiente 'MAX_VARIATION', 'MIN_VARIATION' e/ou 'TIME_TO_NEW_REQUEST' não estão definidas.")

    max_variation = float(max_variation_str)
    min_variation = float(min_variation_str)
    time_to_new_request = int(time_to_new_request_str)

    while True:
        hora_atual = datetime.now().hour

        if hora_inicio <= hora_atual < hora_fim:
            responseExchange = fazer_requisicao()
            if responseExchange:
                create_tweet(responseExchange, client)
            else:
                print(
                    "Não foi possível obter a cotação ou a variação foi menor que o desejado.")
                print("Aguardando 1 minuto antes da próxima requisição...")
            time.sleep(time_to_new_request)
        else:
            print("Fora do horário de operação. Esperando...")
            time.sleep(time_to_new_request)


if __name__ == "__main__":
    bot()
