import requests, json
from config import keys, emoji, symbols

class APIException(Exception):
    pass


class CryptoConverter():
    @staticmethod
    def get_price(values:tuple):
        if len(values) > 3:
            raise APIException(f"Слишком много параметров \
{emoji['eyes']}\nДолжно быть три.")
        elif len(values) < 3:
            raise APIException(f"Слишком мало параметров \
{emoji['eyes']}\nДолжно быть три.")

        base = values[0].lower()
        quote = values[1].lower()
        amount = values[2]

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"{emoji['fearful face']} \
Я пока не знаю такой валюты:\n{base}\n\
Возможно, позже, а пока загляни сюда\n/values")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"{emoji['fearful face']} \
Я пока не знаю такой валюты:\n{quote}\n\
Возможно, позже, а пока загляни сюда\n/values")

        if symbols['comma'] in amount:
            amount = amount.replace(symbols['comma'],
                symbols['point'], 1)

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"{emoji['fearful face']} \
Количество мне совсем не понятно:\n{amount}")

        if base == quote:
            raise APIException(f"\
{emoji['face savouring delicious food']} \
Глупо переводить {base} в {quote}")

        if amount < 0:
            raise APIException(f"{emoji['fearful face']} \
Количество валюты не может быть отрицательным!")

        url = f'https://min-api.cryptocompare.com/data/price?\
fsym={keys[base]}&\
tsyms={keys[quote]}&\
extraParams="Crypto Bot"&\
sign=true'

        r = requests.get(url)

        answer = json.loads(r.content)[keys[quote]]
        answer *= amount
        amount = isInt(amount)
        values = base, quote, amount

        return answer, values


def isInt(n):
    return int(n) if n - int(n) == 0 else n


def declension1(word, amount):
    if word in ('биткоин', 'эфириум', 'доллар', 'фунт', 'зайчик',) :
        if int(amount)%10 == 1: return f'{word}а'
        else:  return f'{word}ов'
    elif word in ('рубль',):
        if int(amount)%10 == 1: return f'{word[:-1]}я'
        else:  return f'{word[:-1]}ей'
    elif word in ('евро', 'песо',):
        return word
    elif word in ('йена', 'вона', 'гривна',):
        if int(amount)%10 == 1: return f'{word[:-1]}ы'
        else:  return word[:-1]
    elif word in ('секунда',):
        if int(amount)%100 in range(11,15): return word[:-1]
        elif int(amount)%10 in range(2,5) : return f'{word[:-1]}ы'
        elif int(amount)%10 == 1: return f'{word[:-1]}у'
        else:  return word[:-1]


def declension2(word):
    if word in ('биткоин', 'эфириум', 'доллар', 'фунт', 'зайчик',):
        return f'{word}ах'
    elif word in ('йена', 'вона', 'гривна',):
        return f'{word}х'
    elif word in ('рубль',):
        return f'{word[:-1]}ях'
    elif word in ('евро', 'песо',):
        return word