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
    #Вот это под вопросом:
    #kpopFille = open('k-pop.txt')
    #kpopdata = kpopFille.readlines()
    #kpopFille.close()
    def updatesoap(self): # метод который обновляет количество игроков
        self.pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text, features="html.parser").find_all('span', class_='num')[0].contents[0]
    def getAmount(self):
        return self.pubg_site
    def updbtc(self):
        self.btcusd = getJsonVal('https://api.coindesk.com/v1/bpi/currentprice.json', ('bpi', 'USD', 'rate'))
    def getAmountBTC(self):
        return self.btcusd

model = Model() # создаём модель


@bot.message_handler(commands=['joke'])
def joke(message: Message):
    soup = BeautifulSoup(requests.get('https://randstuff.ru/joke/').text, features="html.parser")
    JOKE = soup.find(class_="text").contents[0].contents[0].contents[0]
    print('Шутка: ', JOKE) #выдача в консоль
    bot.send_message(message.chat.id, JOKE)


@bot.message_handler(commands=['fact'])
def fact(message: Message):
    soup_f = BeautifulSoup(requests.get('https://randstuff.ru/fact/').text, features="html.parser")
    FACT = soup_f.find(class_="text").contents[0].contents[0].contents[0]
    print('Факт: ', FACT) #выдача в консоль
    bot.send_message(message.chat.id, FACT)


@bot.message_handler(commands=['pubg'])
def pubg(message: Message):
    PUBG = model.getAmount()
    print('Текущий онлайн в PUBG: ', PUBG) #выдача в консоль
    bot.send_message(message.chat.id,'Текущий онлайн в PUBG: ' + PUBG)


@bot.message_handler(commands=['btc'])
def btc(message: Message):
    BTC = model.getAmountBTC()
    print('Курс битка: ', BTC, ' $') #выдача в консоль
    bot.send_message(message.chat.id, 'BTC/USD: ' + BTC + ' $')


@bot.message_handler(commands=['ua'])
def slavaukraine(message: Message):
    print('ОБНАРУЖЕН ХОХОЛ В ЧАТЕ!') #выдача в консоль
    bot.send_message(message.chat.id, 'Героям слава!')


#проверки по массиву еще нет
@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def kpop(message: Message):
    kpopFille = open('k-pop.txt', 'r', encoding='utf-8')
    lines = kpopFille.readlines()
    t1 = message.text
    t1 = t1.split(',')
    for str in lines:
        if  message.text in str: #ПИЗДА, я заебался(((
            bot.send_message(message.chat.id, 'К-поп - ГОВНО!') 
            print('@', message.from_user.username, '- в сообщении юзера обнаружено упоминание к-поп.', 'Тип чата:', message.chat.type) #выдача в консоль
            print('Сообщение юзера:', t1)
            print(lines)


def callbacks():
    model.updatesoap()# функция которая вызывется раз в пять минут в которая запускает все остальные функции
    model.updbtc()

if __name__ == '__main__': # проверка на прямой запуск файла, то есть если добавить его через import эти комманды не будут выполнены
    threading.Timer(300 , callbacks).start()# запуск периодических функцый в отдельном потоке
    bot.polling() # сам запуск бота
    
