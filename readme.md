## Information of keys to connect to Twitter/X api
bearer_token = ""
access_token = ""
access_token_secret = ""
consumer_api_key = ""
consumer_api_key_secret = ""

## Information to operating the bot
url_exchange = "https://economia.awesomeapi.com.br/json/last/EUR-BRL"  # Substitua pela URL da API
init_hour = 9  # Início: 09:00
end_hour = 17  # Fim: 17:00
time_to_new_request = 60  # Espera 1 minuto (60 segundos) entre as requisições
min_variation = -1  # Variação mínima para enviar o tweet
max_variation = 1  # Variação máxima para enviar o tweet