from settings import BOT_TOKEN, BOT_NAME

from telebot import TeleBot, types
from collections import namedtuple
from re import findall, match
from requests import get
from bs4 import BeautifulSoup as bs
from time import strftime, localtime,sleep

import threading

bot = TeleBot(BOT_TOKEN, parse_mode='html')
name = BOT_NAME
hours_await = 20

active = [] #Массив USERID которым должна приходить рассылка

data = {
    'start': f'Привет! Бот <b>{name}</b> делится с вами измененем курса Евро и Доллара с <b>сайта ЦБ</b>.\n\n'
             f'Напишите <b>/go</b> чтоб начать отслеживание',
    "go": f"Начинаю отслеживать для вас курс валюты, отправьте <b>/stop</b> чтоб отключить бота",
    "stop": "Отслеживание прекращено",
    "error": "Не надо писать мне обычный текст, напишите <b>/help</b> для получения списка команд",
    "help": "<b>start</b> - Запустить бота\n<b>go</b> - начать отслеживания валют\n<b>stop</b> - прекратить отслеживание курса",
    "time": "Сводка на сегодня:"
}



def get_currency():
    while True:
        global last_curr
        last_curr = []
        euro = []
        dollar = []
        global history
        history = []
        hour = int(strftime("%H", localtime()))
        if hour >= 15 and hour <= 18:
            day, month, year = strftime("%d %m %Y", localtime()).split()
            for i in range(0,2):
                if i == 1:
                    day = str(int(day)+1)
                for actual_currency in ["Евро", "Доллар США"]:
                    url = f'https://cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'

                    request = get(url)
                    soup = bs(request.text, 'lxml')

                    for tag in soup.findAll('valute'):
                        result = tag.get_text(strip=True)
                        name_of_currency = ' '.join(findall(r'[а-яА-я]+', result))

                        numbers = findall(r'[0-9]+', result)
                        price = (f'{numbers[-2]}.{numbers[-1]}')
                        if actual_currency in name_of_currency:
                            if actual_currency == "Евро":
                                euro.append(price)
                            else:
                                dollar.append(price)

            dollar_new = float('{:.5f}'.format(float(dollar[1])-float(dollar[0])))
            euro_new = float('{:.5f}'.format(float(euro[1])-float(euro[0])))

            if dollar_new == 0.0 and euro_new == 0:
                sleep(60)
            else:
                if dollar_new > 0:
                    dl_message = f"💵\n📈Доллар увеличился на {dollar_new}₽"
                else:
                    dl_message = f"💵\n📉Доллар уменьшился на {dollar_new}₽"
                if euro_new > 0:
                    er_message = f"💶\n📈Евро увеличилось на {euro_new}₽"
                else:
                    er_message = f"💶\n📉Евро уменьшилось на {euro_new}₽"
                message_dollar = f"{dl_message}\nКурс Доллара на Сегодня : {dollar[0]}₽\nКурс Доллара на Завтра: {dollar[1]}₽"
                message_euro = f"{er_message}\nКурс Евро на Сегодня : {euro[0]}₽\nКурс Евро на Завтра: {euro[1]}₽"

                history = ["Сводка по курсу:",message_dollar,message_euro]
                for user_id in active:
                    bot.send_message(user_id,"Сводка по курсу:")
                    bot.send_message(user_id,message_dollar)
                    bot.send_message(user_id,message_euro)

                sleep(hours_await*60*60)
        else:
            sleep(60)
        sleep(1)



threading.Thread(target = get_currency).start()
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, data['start'])

def info(message):
    bot.send_message(message.chat.id, data['time'])
    sleep(2)
    if history == []:
        bot.send_message(message.chat.id, "Сводка на сегодня ещё пустая")
    else:
        for i in history:
            bot.send_message(message.chat.id, i)

@bot.message_handler(commands=['info'])
def info_message(message):
    info(message)


@bot.message_handler(commands=['go'])
def go(message):
    bot.send_message(message.chat.id, data['go'])
    if message.chat.id in active:
        bot.send_message(message.chat.id,"Вы уже подключили отслеживание, если хотите узнать сводку напишите команду /info")
    else:
        active.append(message.chat.id)
        print(f"Юзер {message.chat.id} подключил отслеживание")
        hour = int(strftime("%H", localtime()))
        if hour <= 11 or hour >= 16:
            info(message)

@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, data['stop'])
    active.remove(message.chat.id)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, data['help'])




@bot.message_handler(content_types='text')
def reply(message):
    bot.send_message(message.chat.id, data['error'])

bot.polling(non_stop=True)
