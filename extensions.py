import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException(f"Ошибка API. Код: {response.status_code}")

        data = response.json()
        if quote not in data['rates']:
            raise APIException(f"Валюта {quote} не найдена.")

        try:
            base_amount = data['rates'][quote] * amount
            return base_amount
        except Exception as e:
            raise APIException(f"Ошибка при расчете. Причина: {str(e)}")


