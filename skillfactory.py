
import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException, requests, json

bot = telebot.TeleBot(TOKEN)
keys = {'доллар': 'USD', 'евро': 'EUR', 'рубль': 'RUB'}


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<Имя валюты> <в какую валюту> <количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_command(message):
    text = "Доступные валюты:\n"
    text += "1. доллар\n"
    text += "2. евро\n"
    text += "3. рубль"
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        quote, base, amount = message.text.split(' ')
        amount = float(amount)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка: Неправильный ввод. Убедитесь, что формат верен.")
        return

    if quote not in keys or base not in keys:
        bot.send_message(message.chat.id, "Ошибка: Неправильная валюта. Используйте доллар, евро или рубль.")
        return

    # Формируем URL и отправляем запрос
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')

    if r.status_code != 200:
        bot.send_message(message.chat.id, "Ошибка получения данных. Попробуйте позже.")
        return

    total_base = json.loads(r.content)[keys[base]]
    total_amount = total_base * amount

    text = f'Цена {amount} {quote} в {base} - {total_amount:.2f}'
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling()



