import telebot
from config import keys, TOKEN, emoji, flags
from extensions import APIException, CryptoConverter, declension1, declension2

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help',])
def startHelp(message: telebot.types.Message):
    text1 = 'Ой, кто это? Так это же'
    text2 = f"{emoji['smiling face with heart-shaped eyes']}\n\
Категорически тебя приветствую!\
\n\n\
Это бот-конвертер валют.\n\
Для начала работы введи команду в формате: \n\
    <из какой валюты переводим> \n\
    <в какую переводим> \n\
    <количество денюшков>\n\
Например: евро доллар 1.15\n\n\
Список доступных валют: /values\n\n\
А если наболело - выскажись в голосовом сообщении, \
я выслушаю {emoji['ear']} {emoji['speak-no-evil monkey']}"
    bot.reply_to(message,
        f'{text1} {message.chat.first_name}! {text2}')


@bot.message_handler(commands=['values',])
def values(message: telebot.types.Message):
    text = f"{emoji['white heavy check mark']} \
Доступные валюты:"
    for key in keys:
        flag = flags.get(keys[key]) or ''
        text = '\n- '.join((text, key)) + f' {flag}'
    text += f"\n\n{emoji['white heavy check mark']} \
Названия валют вводятся в именительном падеже \
единственного числа.\n\
Регистр символов не имеет значения."
    bot.reply_to(message,
        text)


@bot.message_handler(content_types=['text',])
def text(message: telebot.types.Message):
    try:
        values = message.text.split()
        answer, values = CryptoConverter.get_price(values)
        base, quote, amount = values
    except APIException as e:
        bot.reply_to(message,
            f"Ошибка пользователя {emoji['no entry']}\n{e}")
    except Exception as e:
        bot.reply_to(message,
            f"Не удалось обработать команду \
{emoji['pile of poo']}\n{e}")
    else:
        text = f"{emoji['chart with upwards trend']} \
Стоимость {amount} {declension1(base, amount)} \
в {declension2(quote)} - {answer}"
        bot.reply_to(message,
            text)


@bot.message_handler(content_types=['voice',])
def voice(message):
    bot.reply_to(message,\
f"Какой голос приятный \
{emoji['smiling face with smiling eyes']}\n\
Жаль только, длился {message.voice.duration} \
{declension1('секунда', message.voice.duration)}.\n\
Так бы слушал и слушал...")


bot.polling()