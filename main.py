import random
import logging
import time, threading
import pickle
import telebot
from telebot import types
from telebot.types import Message
from telegram.ext import Updater, CommandHandler
from bs4 import BeautifulSoup
from datetime import datetime
import requests

TOKEN = '771027063:AAHjnTSc5uH5BapuPAHsHwuKiN7VaQludzc' #токен бота
bot = telebot.TeleBot(TOKEN)
USERS = set() 

@bot.message_handler(commands=['pubg', 'joke', 'btc', 'fact', 'slavaukraine'])
def command_handler(message: Message):
    bot.send_message(message.chat.id, 'в разработке, петушара')


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def echo_digits(message: Message):
    print(message.from_user.id)
    if 'кпоп' or 'к-поп' or 'Кпоп' in message.text:
        bot.send_message(message.chat.id, 'К-поп - ГОВНО!')    

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

def pubg(message: Message):
    bot.reply_to(message,'Текущий онлайн в PUBG: ' + str(model.getAmount()))  

def joke(message: Message):
    soup = BeautifulSoup(requests.get('https://randstuff.ru/joke/').text, features="html.parser")
    joke = soup.find(class_="text").contents[0].contents[0].contents[0]
    bot.sendMessage(message, text=str(joke))

@bot.message_handler(commands=['fact'])
def fact(message: Message):
    soup_f = BeautifulSoup(requests.get('https://randstuff.ru/fact/').text, features="html.parser")
    fact = soup_f.find(class_="text").contents[0].contents[0].contents[0]
    bot.send_message(message.chat.id, text=str(fact))

def slavaukraine(message: Message):
    bot.sendMessage(message, text='Героям слава!')

def btc(message: Message):
    bot.sendMessage(message, text='BTC/USD: ' + str(model.getAmountBTC()) + ' $')  

def callbacks():
    model.updatesoap()# функция которая вызывется раз в пять минут в которая запускает все остальные функции
    model.updbtc()
if __name__ == '__main__': # проверка на прямой запуск файла, то есть если добавить его через import эти комманды не будут выполнены
    threading.Timer(300 , callbacks).start()# запуск периодических функцый в отдельном потоке
    bot.polling() # сам запуск бота
    
