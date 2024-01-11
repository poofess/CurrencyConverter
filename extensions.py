import requests
import json
from config import keys


class ConversionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ConversionException(f'Недопустимое значение. Пожалуйста, введите положительное число, отличное от нуля.')
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}. Пожалуйста, введите числовое значение.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount
