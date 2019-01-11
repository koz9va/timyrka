import random
import logging
import time, threading
import telebot
from telebot import types
from telebot.types import Message
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import mclass

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
    kpop = ('кпоп', 'к-поп', 'Кпоп', 'К-поп')
    # в следующей строке делаем запрос на сайт с количеством игроков и скрапим его через beautiful soup
    pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text, features="html.parser").find_all('span', class_='num')[0].contents[0]
    btcusd = getJsonVal('https://api.coindesk.com/v1/bpi/currentprice.json', ('bpi', 'USD', 'rate'))
    helloFile = open('hello.txt', 'r')
    hellodata = helloFile.readlines() # открывем файл и создаём массив со строками приветствия
    helloFile.close()
    msg = mclass.MessWork('UsrsBd.pkl')
    messStore = open('messages.txt', 'a')
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
    def sendTo(self, cmsg):
        for usr in self.msg.Users:
            if usr.name == cmsg.To:
                if cmsg.author in usr.blocked:
                    return False
                else:
                    bot.send_message(usr.chatId, 'От '+ cmsg.authName+': '+cmsg.text)
                    usr.last = cmsg.author
                    usr.lastName = cmsg.authName
                    with open('messages.txt', 'a') as messStore:
                        messStore.write('\n##########\n')
                        messStore.write('From '+usr.lastM.author+' as '+usr.lastM.authName+' , To: ' + usr.lastM.To+'\n')
                        messStore.write('Text: '+usr.lastM.text)
                        messStore.close()
                    model.msg.save()
                    return True
        return False
model = Model() # создаём модель

@bot.message_handler(commands=['start', 'help'])
def start(message: Message):
    hello = open('hello.txt', 'r')
    hellotext = hello.readline()
    bot.send_message(message.chat.id, hellotext)
    hello.close()
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
    print('Текущий онлайн в PUBG: онлайн', PUBG) #выдача в консоль
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

@bot.message_handler(commands=['getIn'])
def getinchat(message: Message):
    if message.chat.type == 'private':
        notadd = False
        for user in model.msg.Users:
            if str(user.name) == '@'+str(message.from_user.username):
                notadd = True
                break
            if notadd == False:
                model.msg.start(mclass.User(message.chat.id, message.from_user.username))
                bot.send_message(message.chat.id, '@'+str(message.from_user.username)+' теперь может принимать сообщения')
                print(message.chat.id)
                print('@'+message.from_user.username)
            else:
                bot.send_message(message.chat.id, 'Вы уже зарегестрированы')
    else:
        bot.reply_to(message, 'не палися, всі ж дивляться')
@bot.message_handler(commands=['block'])
def ask0(message: Message):
    if message.chat.type == 'private':
        for usr in model.msg.Users:
            if '@'+str(message.from_user.username) == usr.name:
                msg = bot.reply_to(message, 'Вы уверены что хотите заблокировать '+ usr.lastName+'? если да то напишите "Y" без скобочек, если нет то всё остальное')
                bot.register_next_step_handler(msg, accept0)
                break
    else:
        bot.reply_to(message, 'не палися, всі ж дивляться')
def accept0(message: Message):
    for usr in model.msg.Users: # нужно придумать как убрать это прожордивое безобразие
        if '@'+str(message.from_user.username) == usr.name:
            if str(message.text == 'Y'):
                usr.blocked.append(usr.last)
                bot.send_message(message.chat.id, 'пользователь '+ usr.lastName+' заблокирован')
                model.msg.save()
@bot.message_handler(commands=['reply'])
def replyTo(message: Message):
    if message.chat.type == 'private':
        for usr in model.msg.Users:
            if '@'+str(message.from_user.username) == usr.name:
                msg = bot.reply_to(message, 'чтобы ответить '+usr.lastName+' напишите Y, в другом случае всё остальное')
                bot.register_next_step_handler(msg, nextreply0)
                break
    else:
        bot.reply_to(message, 'не палися, всі ж дивляться')
def nextreply0(message: Message):
    for usr in model.msg.Users:
        if '@'+str(message.from_user.username) == usr.name:
            if message.text == 'Y':
                usr.lastM.To = '@'+str(usr.last)
                textm(message)
                break
            else:
                bot.send_message(message.chat.id, 'Ок')

@bot.message_handler(commands=['unblock'])
def unblock(message: Message):
    if message.chat.type == 'private':
        for usr in model.msg.Users:
            if usr.name == '@'+message.from_user.username:
                bot.send_message(message.chat.id, 'Вы заблокировали: \n'+ str(u+'\n' for u in usr.blocked))
                print(u+'\n' for u in usr.blocked)
                break
    else:
        bot.reply_to(message, 'не палися, всі ж дивляться')

@bot.message_handler(commands=['send'])
def sendMess(message: Message):
    if message.chat.type == 'private':
        msg = bot.reply_to(message, 'Адресат:')
        bot.register_next_step_handler(msg, tom)
    else:
        bot.reply_to(message, 'не палися, всі ж дивляться')

def auth(message):
    if len(str(message.text)) > 20:
        msg = bot.reply_to(message, 'не больше 20 символов')
        bot.register_next_step_handler(msg ,auth)
    else:
        for usr in model.msg.Users:
            if usr.name == '@'+message.from_user.username:
                usr.lastM.authName = message.text
                usr.lastM.author = message.from_user.username
                if usr.sentToUsr < 10:
                    if usr.lastM.To not in usr.sentUsrs:
                        usr.sentUsrs.append(message.text)
                        usr.sentToUsr += 1
                    if model.sendTo(usr.lastM) == False:
                        bot.send_message(message.chat.id, 'Этот пользователь заблокировал вас, или вы непрввильно указали ник, или этот пользователь не зарегистрирован в нашей системе')
                    else:
                        bot.send_message(message.chat.id, 'Сообщение отправлено')
                else:
                    inlist = False
                    for tousr in model.msg.TooUsers:
                        if tousr[0] == message.from_user.username:
                            inlist = True
                            break
                    if not inlist:
                        model.msg.TooUsers.append([message.from_user.username, 300])    
                    bot.send_message(message.chat.id, 'Вы уже написали максимальному количеству пользователей, подождите максимум 5 минут')

def textm(message):
    if len(str(message.text)) > 300:
        msg = bot.reply_to(message, 'не больше 300 символов')
        bot.register_next_step_handler(msg , textm)
    else:
        for usr in model.msg.Users:
            if usr.name == '@'+message.from_user.username:
                usr.lastM.text = message.text
                break
        msg = bot.reply_to(message, 'Условное имя автора:')
        bot.register_next_step_handler(msg, auth)

def tom(message):
    check = list(message.text)
    if check[0] == '@':
        for usr in model.msg.Users:
            if usr.name == '@'+message.from_user.username:
                usr.lastM.To = message.text
                break
        msg = bot.reply_to(message, 'Послание: ')
        bot.register_next_step_handler(msg, textm)
    else:
        msg = bot.reply_to(message, 'ник должен начинаться с @')
        bot.register_next_step_handler(msg, tom)
#проверки по массиву еще нет
#нужно научить этого придурка работать в конфе


def callbacks():
    model.updatesoap()# функция которая вызывется раз в пять минут в которая запускает все остальные функции
    model.updbtc()
    model.msg.save()

def timers():
    for usr in range(0,len(model.msg.TooUsers)-1):
        if model.msg.TooUsers[usr][1] <= 0:
            del model.msg.TooUsers[usr]
        model.msg.TooUsers[usr][1] += 1
if __name__ == '__main__': # проверка на прямой запуск файла, то есть если добавить его через import эти комманды не будут выполнены
    threading.Timer(300 , callbacks).start()# запуск периодических функцый в отдельном потоке
    threading.Timer(1, timers)
    bot.polling() # сам запуск бота