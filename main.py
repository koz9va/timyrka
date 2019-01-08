import random
import logging
import time, threading
from telegram.ext import Updater, CommandHandler
from bs4 import BeautifulSoup
import requests
def getJsonVal(link = str(), path = list()): # функция которая принимает строку ссылки и "путь" к данным в json
        jsonResponce = requests.get(link).json() # а потом возваращет готовый результат
        for step in path: # нужно подумать что делать в том случае если на пути будет массив
            jsonResponce = jsonResponce[step]
        return jsonResponce
class Model(): # класс в котором храннятся все данные которые мы передаём пользователям
    timer = int()
    # в следующей строке делаем запрос на сайт с количеством игроков и скрапим его через beautiful soup
    pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text, features="html.parser").find_all('span', class_='num')[0].contents[0]
    btcusd = getJsonVal('https://api.coindesk.com/v1/bpi/currentprice.json', ('bpi', 'USD', 'rate'))
    helloFile = open('hello.txt', 'r')
    hellodata = helloFile.readlines() # открывем файл и создаём массив со строками приветствия
    helloFile.close()
    def updatesoap(self): # метод который обновляет количество игроков
        self.pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text, features="html.parser").find_all('span', class_='num')[0].contents[0]
    def getAmount(self):
        return self.pubg_site
    def updbtc(self):
        self.btcusd = getJsonVal('https://api.coindesk.com/v1/bpi/currentprice.json', ('bpi', 'USD', 'rate'))
    def getAmountBTC(self):
        return self.btcusd

model = Model() # создаём модель

def hello(bot, update):
    rn = random.randint(0, len(model.hellodata)) # генерируем случайный номер строки
    update.message.reply_text(
        'Привет, {}!'.format(update.message.from_user.first_name)
    )
    bot.sendMessage(chat_id=update.message.chat_id, text=model.hellodata[rn]) # отправляем случайный елемент масива
updater = Updater('771027063:AAHjnTSc5uH5BapuPAHsHwuKiN7VaQludzc') # токен бота
def pubg(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Текущий онлайн в PUBG: ' + str(model.getAmount()))

def joke(bot, update):
    soup = BeautifulSoup(requests.get('https://randstuff.ru/joke/').text, features="html.parser")
    joke = soup.find(class_="text").contents[0].contents[0].contents[0]
    bot.sendMessage(chat_id=update.message.chat_id, text=str(joke))

def fact(bot, update):
    soup_f = BeautifulSoup(requests.get('https://randstuff.ru/fact/').text, features="html.parser")
    fact = soup_f.find(class_="text").contents[0].contents[0].contents[0]
    bot.sendMessage(chat_id=update.message.chat_id, text=str(fact))

def slavaukraine(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Героям слава!')

def btc(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='BTC/USD: ' + str(model.getAmountBTC()) + ' $')

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('pubg', pubg))
updater.dispatcher.add_handler(CommandHandler('joke', joke))
updater.dispatcher.add_handler(CommandHandler('fact', fact))
updater.dispatcher.add_handler(CommandHandler('slavaukraine', slavaukraine))
updater.dispatcher.add_handler(CommandHandler('btc', btc))

def callbacks():
    model.updatesoap()# функция которая вызывется раз в пять минут в которая запускает все остальные функции
    model.updbtc()
if __name__ == '__main__': # проверка на прямой запуск файла, то есть если добавить его через import эти комманды не будут выполнены
    threading.Timer(300 , callbacks).start()# запуск периодических функцый в отдельном потоке
    updater.start_polling() # сам запуск бота
    updater.idle()
