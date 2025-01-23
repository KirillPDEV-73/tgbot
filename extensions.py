import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        url = f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}'
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException(f"Ошибка API. Код: {response.status_code}")

        data = response.json()
        if quote not in data['rates']:
            raise APIException(f"Валюта {quote} не найдена.")

        try:
            base_amount = data['rates'][quote] * amount
        except KeyError:
            raise APIException(f"Валюта {base} не найдена.")

        return base_amount

