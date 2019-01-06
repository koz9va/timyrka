import random
import logging
import time, threading
from telegram.ext import Updater, CommandHandler
from bs4 import BeautifulSoup
import requests

class Model(): # класс в котором храннятся все данные которые мы передаём пользователям
    timer = int()
    # в следующей строке делаем запрос на сайт с количеством игроков и скрапим его через beautiful soup
    pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text, features="html.parser").find_all('span', class_='num')[0].contents[0]
    btcusd = BeautifulSoup(requests.get('https://prometheus.ru/coins/btc/').text, features="html.parser").find_all('span', class_='currency-value rc-PRICE-BTC', id='js-table-coin-value')[0].contents[0]
    helloFile = open('hello.txt', 'r')
    hellodata = helloFile.readlines() # открывем файл и создаём массив со строками приветствия
    helloFile.close()
    def updatesoap(self): # метод который обновляет количество игроков
        self.pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text, features="html.parser").find_all('span', class_='num')[0].contents[0]
    def getAmount(self):
        return self.pubg_site
    def updbtc(self):
        self.btcusd = BeautifulSoup(requests.get('https://prometheus.ru/coins/btc/').text, features="html.parser").find_all('span', class_='currency-value rc-PRICE-BTC', id='js-table-coin-value')[0].contents[0]    
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
    bot.sendMessage(chat_id=update.message.chat_id, text='Ебанная шутка')

def btc(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='BTC/USD: ' + str(model.getAmountBTC()) + '$')    

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('pubg', pubg))
updater.dispatcher.add_handler(CommandHandler('joke', joke))
updater.dispatcher.add_handler(CommandHandler('btc', btc))

def callbacks():
    model.updatesoap()# функция которая вызывется раз в пять минут в которая запускает все остальные функции

if __name__ == '__main__': # проверка на прямой запуск файла, то есть если добавить его через import эти комманды не будут выполнены
    threading.Timer(300 , callbacks).start()# запуск периодических функцый в отдельном потоке
    updater.start_polling() # сам запуск бота
    updater.idle()
