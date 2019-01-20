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
import json
import urllib.request

TOKEN = 'YOURTOKEN' #токен бота
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
    msg = mclass.MessWork('Usrs')
    kpopdata = ['KPOP', 'кпопу', 'К-поп', 'к-поп', 'кпоп', 'k-pop', 'K-pop', 'КПОП', 'К-ПОП', 'Кпоп', 'BTS', 'BTs', 'bTS', 'bts', 'b.t.s', 'Ким Намджун', 'Намджун', 'корейский поп', 'к.п.о.п', 'Ким Техен', 'Ким Техён', 'Техен', 'кпоа', 'кпопер', 'Bts', 'бтс', 'Бтс', 'БТС']
    kpopFille = open('k-pop.txt', 'r', encoding='utf-8')
    kpopans = kpopFille.readlines()
    kpopFille.close()
    kpopstdata = []
    kpopchats_blacklist = []
    all_group_name = []
    all_group_id = []
    all_group_type = []
    emili_trig = [2, 4, 8]
    now = datetime.now()
    now_massiv = [now.day, now.month, now.year]
    fixerdt = [0, 0, 0, 0]
    smtgmcid = [0]    
    with open('kpop_sticker_id.txt') as f:
        kpopstdata = f.read().splitlines()
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
                    bot.send_message(usr.chatId, 'От '+ cmsg.authName+': '+cmsg.text+ '\n Чтобы заблокировать этого пользователя /block , чтобы ответить /reply')
                    usr.last = cmsg.author
                    usr.lastName = cmsg.authName
                    with open('messages.txt', 'a') as messStore:
                        messStore.write('\n##########\n')
                        messStore.write('From '+usr.lastM.author+' as '+usr.lastM.authName+' , To: ' + usr.lastM.To+'\n')
                        messStore.write('Text: '+usr.lastM.text+'\n')
                        currentDT = datetime.now()
                        currentDT = currentDT.strftime("%Y-%m-%d %H:%M:%S")
                        messStore.write('Date: '+currentDT)
                        messStore.close()
                    model.msg.save()
                    return True
        return False
model = Model() # создаём модель


@bot.message_handler(commands=['start'])
def start(message: Message):
    startru = open('start.txt', 'r', encoding='utf-8')
    startru1 = startru.readline()
    bot.send_message(message.chat.id, startru1)
    startru.close()
    mcid = message.chat.id
    mctype = message.chat.type
    if mctype == 'group' or mctype == 'supergroup':
        if mcid not in model.all_group_id:
            model.all_group_id.append(message.chat.id)
            model.all_group_name.append(message.chat.title)
            model.all_group_type.append(message.chat.type)
        else:
            pass   

@bot.message_handler(commands=['help'])
def c_help(message: Message):
    #print('Пользователь @', message.from_user.username, 'запросил помощь.') #выдача в консоль
    bot.send_message(message.chat.id, 'Список команд:\n'
    '/start - Приветсвие\n'
    '/help - Помощь\n'
    '/getin - Регистрация для приема/отправки анонимных сообщений\n'
    '/send - Отправка анонимных сообщений\n'
    '/reply - Команда для ответа на анонимное сообщение\n'
    '/block - Команда для блокировки анонимного отправителя\n'
    '/joke - Dolbobot пошутит\n'
    '/fact - Dolbobot поделится фактом\n'
    '/pubg - Текущий онлайн в ПУБГ\n'
    '/rates - Курсы валют\n'
    '/btc - Курс Bitcoin\n'
    '/binary - Перевод чисел из десятичной системы счисления в двоичную.')
    mcid = message.chat.id
    mctype = message.chat.type
    if mctype == 'group' or mctype == 'supergroup':
        if mcid not in model.all_group_id:
            model.all_group_id.append(message.chat.id)
            model.all_group_name.append(message.chat.title)
            model.all_group_type.append(message.chat.type)
        else:
            pass   

@bot.message_handler(commands=['fact'])
def fact(message: Message):
    soup_f = BeautifulSoup(requests.get('https://randstuff.ru/fact/').text, features="html.parser")
    FACT = soup_f.find(class_="text").contents[0].contents[0].contents[0]
    #print('Факт: ', FACT) #выдача в консоль
    bot.send_message(message.chat.id, FACT)
    mcid = message.chat.id
    mctype = message.chat.type
    if mctype == 'group' or mctype == 'supergroup':
        if mcid not in model.all_group_id:
            model.all_group_id.append(message.chat.id)
            model.all_group_name.append(message.chat.title)
            model.all_group_type.append(message.chat.type)
        else:
            pass   
@bot.message_handler(commands=['joke'])
def joke(message: Message):
    soup = BeautifulSoup(requests.get('https://randstuff.ru/joke/').text, features="html.parser")
    JOKE = soup.find(class_="text").contents[0].contents[0].contents[0]
    #print('Шутка: ', JOKE) #выдача в консоль
    bot.send_message(message.chat.id, JOKE)
    mcid = message.chat.id
    mctype = message.chat.type
    if mctype == 'group' or mctype == 'supergroup':
        if mcid not in model.all_group_id:
            model.all_group_id.append(message.chat.id)
            model.all_group_name.append(message.chat.title)
            model.all_group_type.append(message.chat.type)
        else:
            pass   

@bot.message_handler(commands=['pubg'])
def pubg(message: Message):
    PUBG = model.getAmount()
    #print('Текущий онлайн в PUBG: ', PUBG) #выдача в консоль
    bot.send_message(message.chat.id,'Текущий онлайн в PUBG: ' + PUBG)
    mcid = message.chat.id
    mctype = message.chat.type
    if mctype == 'group' or mctype == 'supergroup':
        if mcid not in model.all_group_id:
            model.all_group_id.append(message.chat.id)
            model.all_group_name.append(message.chat.title)
            model.all_group_type.append(message.chat.type)
        else:
            pass   

@bot.message_handler(commands=['btc'])
def btc(message: Message):
    BTC = model.getAmountBTC()
    #print('Курс битка: ', BTC, ' $') #выдача в консоль
    bot.send_message(message.chat.id, 'BTC/USD: ' + BTC + ' $')
    mcid = message.chat.id
    mctype = message.chat.type
    if mctype == 'group' or mctype == 'supergroup':
        if mcid not in model.all_group_id:
            model.all_group_id.append(message.chat.id)
            model.all_group_name.append(message.chat.title)
            model.all_group_type.append(message.chat.type)
        else:
            pass   
@bot.message_handler(commands=['rates'])
def fixer_rates(message: Message):
    #такое ебанутое разветление дальше обусловлено тем, что курсы валют особо не меняются в течении одного дня
    #также API данного сервиса по фри тарифу дает только 1000 запросов в месяц
    #если бот запущен на тесте, не используйте эту функцию просто так
    #рассчитано на то, что бот будет работать 24/7 и обновлять инфу о курсах валют только раз в сутки 
    local_f_time=datetime.now() 
    fd=local_f_time.day 
    fm=local_f_time.month 
    fy=local_f_time.year 
    fdfmfy = [fd, fm, fy] 
    if fdfmfy == model.now_massiv and model.fixerdt[0] != 0 and model.fixerdt[1] != 0 and model.fixerdt[2] != 0 and model.fixerdt[3] == 1:
        USDUAH = model.fixerdt[0]
        EURUAH = model.fixerdt[1]
        RUBUAH = model.fixerdt[2]
        bot.send_message(message.chat.id, 'Курсы валют:\n' + '\nUSD/UAH: ' + USDUAH + '\nEUR/UAH: ' + EURUAH+ '\nRUB/UAH: ' + RUBUAH)
    elif model.fixerdt[3] == 0:
        f01 = 1
        urleur_d = requests.get('http://data.fixer.io/api/latest?access_key=9bf1e25b1208f9a4c153142e023a3710&format=1')
        eur_d = urleur_d.json()['rates']['UAH']
        usd_d = urleur_d.json()['rates']['USD']
        rub_d = urleur_d.json()['rates']['RUB']
        usd_c_d = float(eur_d)/float(usd_d)
        rub_c_d = float(eur_d)/float(rub_d)
        usd = round(float(usd_c_d), 2)
        eur = round(float(eur_d), 2)
        rub = round(float(rub_c_d), 2)
        model.fixerdt[0] = str(usd)
        model.fixerdt[1] = str(eur)
        model.fixerdt[2] = str(rub)
        USDUAH = model.fixerdt[0]
        EURUAH = model.fixerdt[1]
        RUBUAH = model.fixerdt[2]
        bot.send_message(message.chat.id, 'Курсы валют:\n' + '\nUSD/UAH: ' + USDUAH + '\nEUR/UAH: ' + EURUAH+ '\nRUB/UAH: ' + RUBUAH)
        model.fixerdt[3] = f01
    elif fdfmfy != model.now_massiv:
        urleur_d = requests.get('http://data.fixer.io/api/latest?access_key=9bf1e25b1208f9a4c153142e023a3710&format=1')
        eur_d = urleur_d.json()['rates']['UAH']
        usd_d = urleur_d.json()['rates']['USD']
        rub_d = urleur_d.json()['rates']['RUB']
        usd_c_d = float(eur_d)/float(usd_d)
        rub_c_d = float(eur_d)/float(rub_d)
        usd = round(float(usd_c_d), 2)
        eur = round(float(eur_d), 2)
        rub = round(float(rub_c_d), 2)
        model.fixerdt[0] = str(usd)
        model.fixerdt[1] = str(eur)
        model.fixerdt[2] = str(rub)
        USDUAH = model.fixerdt[0]
        EURUAH = model.fixerdt[1]
        RUBUAH = model.fixerdt[2]
        bot.send_message(message.chat.id, 'Курсы валют:\n' + '\nUSD/UAH: ' + USDUAH + '\nEUR/UAH: ' + EURUAH+ '\nRUB/UAH: ' + RUBUAH)
        model.now_massiv[0] = fd
        model.now_massiv[1] = fm
        model.now_massiv[2] = fy

@bot.message_handler(commands=['binary'])
def conv_to_binary(message: Message):
    #print('Перевод в двоичную систему счисления.') #выдача в консоль
    bot.send_message(message.chat.id, 'Введите натуральное число:')   
    bot.register_next_step_handler(message, converter)
def converter(message: Message):   
    conv_data = message.text
    if conv_data.isdigit() == True:    
        conv = int(conv_data)
        result = ''
        while conv > 0:
            y = str(conv % 2)
            result = y + result
            conv = int(conv / 2)    
        #print('10ССЧ:', int(conv_data), ' - 2ССЧ:', result)
        bot.send_message(message.chat.id, 'Число ' + conv_data + ' в двоичной системе счисления: ' + result)
    else:
        bot.send_message(message.chat.id, 'Натуральное число не было получено!\n'
         '/binary - для перезапуска функции.\n'
         '/info_naturalis - информация о натуральных числах.')
@bot.message_handler(commands=['info_naturalis'])
def info_naturalis(message: Message):
    bot.send_message(message.chat.id, 'Натуральные числа — числа, возникающие естественным образом при счёте. Последовательность всех натуральных чисел, расположенных в порядке возрастания, называется натуральным рядом. ')
    #сасать реал ыыы
    #сасать реал ыыы
    #сасать реал ыыы

    

@bot.message_handler(commands=['getin'])
def getinchat(message: Message):
    if message.chat.type == 'private':
        if message.from_user.username is None:
            bot.send_message(message.chat.id, 'Отсутствует имя пользователя. Пожалуйста, создайте его!')
        else:
            notadd = False
            for user in model.msg.Users:
                # print(user.name)
                if str(user.name) == '@'+str(message.from_user.username):
                    notadd = True
                    break
            if notadd == False:
                model.msg.start(mclass.User(message.chat.id, str(message.from_user.username)))
                bot.send_message(message.chat.id, '@'+str(message.from_user.username)+' теперь может принимать сообщения.')
                print(message.chat.id)
                print('@'+message.from_user.username)
            else:
                bot.send_message(message.chat.id, 'Вы уже зарегестрированы')
    else:
        bot.reply_to(message, 'Не советую использовать эту функцию в публичном чате.')
@bot.message_handler(commands=['block'])
def ask0(message: Message):
    if message.chat.type == 'private':
        for usr in model.msg.Users:
            if '@'+str(message.from_user.username) == usr.name:
                msg = bot.reply_to(message, 'Вы уверены что хотите заблокировать '+ usr.lastName+'? если да то напишите "Y" без скобочек, если нет то всё остальное')
                bot.register_next_step_handler(msg, accept0)
                break
    else:
        bot.reply_to(message, 'Не советую использовать эту функцию в публичном чате.')
def accept0(message: Message):
    if str(message.text) == 'Y':
        for usr in model.msg.Users: # нужно придумать как убрать это прожордивое безобразие
            if '@'+str(message.from_user.username) == usr.name:
                usr.blocked.append(usr.last)
                bot.send_message(message.chat.id, 'Пользователь '+ usr.lastName+' заблокирован.')
                model.msg.save()
    else:
        bot.send_message(message.chat.id, 'Ок')
@bot.message_handler(commands=['reply'])
def replyTo(message: Message):
    if message.chat.type == 'private':
        for usr in model.msg.Users:
            if '@'+str(message.from_user.username) == usr.name:
                msg = bot.reply_to(message, 'Чтобы ответить '+usr.lastName+' напишите Y. Если не хотите отвечать - проигнорируйте просьбу.')
                bot.register_next_step_handler(msg, nextreply0)
                break
    else:
        bot.reply_to(message, 'Не советую использовать эту функцию в публичном чате.')
def nextreply0(message: Message):
    for usr in model.msg.Users:
        if '@'+str(message.from_user.username) == usr.name:
            if message.text == 'Y':
                usr.lastM.To = '@'+str(usr.last)
                msg = bot.reply_to(message, 'Послание: ')
                bot.register_next_step_handler(msg, textm)
                break
            else:
                bot.send_message(message.chat.id, 'Ок.')

@bot.message_handler(commands=['unblock'])
def unblock(message: Message):
    if message.chat.type == 'private':
        for usr in model.msg.Users:
            if usr.name == '@'+message.from_user.username:
                bot.send_message(message.chat.id, 'Вы заблокировали: \n'+ str(u+'\n' for u in usr.blocked))
                ##print(u+'\n' for u in usr.blocked)
                break
    else:
        bot.reply_to(message, 'Не советую использовать эту функцию в публичном чате.')
@bot.message_handler(commands=['send'])
def sendMess(message: Message):
    if message.chat.type == 'private':
        msg = bot.reply_to(message, 'Адресат:')
        bot.register_next_step_handler(msg, tom)
    else:
        bot.reply_to(message, 'Не советую использовать эту функцию в публичном чате.')

def auth(message):
    if len(str(message.text)) > 20:
        msg = bot.reply_to(message, 'Не более 20 символов!')
        bot.register_next_step_handler(msg ,auth)
    else:
        for usr in model.msg.Users:
            if usr.name == '@'+message.from_user.username:
                usr.lastM.authName = message.text
                usr.lastM.author = message.from_user.username
                if True:
                    # if usr.lastM.To not in usr.sentUsrs:
                    #     usr.sentUsrs.append(message.text)
                    #     usr.sentToUsr += 1
                    if model.sendTo(usr.lastM) == False:
                        bot.send_message(message.chat.id, 'Этот пользователь заблокировал вас или вы непрввильно указали ник. Возможно этот пользователь не зарегистрирован в нашей системе.')
                    else:
                        bot.send_message(message.chat.id, 'Сообщение отправлено!')
               # else:
                    # inlist = False
                    # for tousr in model.msg.TooUsers:
                    #     if tousr[0] == message.from_user.username:
                    #         inlist = True
                    #         break
                    #  if not inlist:
                    #     model.msg.TooUsers.append([message.from_user.username, 300])    
                    # bot.send_message(message.chat.id, 'Вы уже написали максимальному количеству пользователей, подождите максимум 5 минут')

def textm(message):
    if len(str(message.text)) > 300:
        msg = bot.reply_to(message, 'Не более 300 символов!')
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
        msg = bot.reply_to(message, 'Ник должен начинаться с "@"!')
        bot.register_next_step_handler(msg, tom)


@bot.message_handler(commands=['notify'])
def notif(message: Message):
    if str(message.from_user.username) == 'koz9va' or str(message.from_user.username) == 'r4mpagelowe':
        msg = bot.reply_to(message, 'Text of notification for all users:')
        bot.register_next_step_handler(msg, notify)
    else:
        bot.reply_to(message, 'У вас отсутствуют достаточные полномочия для использования этой функции.')   
def notify(message):
    for user in model.msg.Users:
        bot.send_message(user.chatId, message.text)

#Вывод chat_id групп и супергрупп в которых работает бот
@bot.message_handler(commands=['groups_cid'])
def groups_cid(message: Message):
    if str(message.from_user.username) == 'koz9va' or str(message.from_user.username) == 'r4mpagelowe':
        gcid = len(model.all_group_id)
        from beautifultable import BeautifulTable
        table = BeautifulTable()
        table.column_headers = ['Chat_name', 'Chat_id', 'Chat_type']
        for a in range(gcid):    
            table.append_row([model.all_group_name[a], model.all_group_id[a], model.all_group_type[a]])
            a = a + 1
        print(table)
        table_text = str(table)
        bot.reply_to(message, table_text)        
    else:
        bot.reply_to(message, 'У вас отсутствуют достаточные полномочия для использования этой функции.') 

#отправка сообщения в конкретный чат
@bot.message_handler(commands=['send_to_group'])
def sendMessToGroup(message: Message):
    if str(message.from_user.username) == 'koz9va' or str(message.from_user.username) == 'r4mpagelowe':
        if message.chat.type == 'private':
            bot.send_message(message.chat.id, 'Введите Chat_id:')
            bot.register_next_step_handler(message, smtg)
        else:
            bot.reply_to(message, 'Мой господин, для использования этой функции напишите мне в лс.')            
    else:
        bot.reply_to(message, 'У вас отсутствуют достаточные полномочия для использования этой функции.')         
def smtg(message: Message):
    model.smtgmcid[0] = str(message.text)
    bot.send_message(message.chat.id, 'Отлично. Теперь напишите то, что хотели бы отправить:')
    bot.register_next_step_handler(message, smtg1)
def smtg1(message: Message):
    msgtxt = message.text
    mcid = model.smtgmcid[0]
    bot.send_message(message.chat.id, 'Сообщение успешно отправлено!')
    bot.send_message(mcid, msgtxt)

#старт-стоп
@bot.message_handler(commands=['start_kpop'])
def start_kpop(message: Message):
    if message.chat.id in model.kpopchats_blacklist:
        model.kpopchats_blacklist.remove(message.chat.id)
        bot.send_message(message.chat.id, 'Cлежение за IQ восстановлено!')
@bot.message_handler(commands=['stop_kpop'])
def stop_kpop(message: Message):
    if message.chat.id not in model.kpopchats_blacklist:
        model.kpopchats_blacklist.append(message.chat.id)
        bot.send_message(message.chat.id, 'Слежение за IQ остановлено!')

#регулярное пиветствие в 10 утра в группах и супергруппах.
def morning10():
    local_m_time=datetime.now() 
    mh=local_m_time.hour 
    mm=local_m_time.minute  
    mhmm = [mh, mm]
    #print(mhmm)
    #print(model.all_group_id)
    for word in model.all_group_id:
        mcid = str(word)
        if mhmm[0] == 10 and mhmm[1] == 0:
            bot.send_message(mcid, 'ЧЕ СПИМ БЛЯТЬ, ПЕТУШАРЫ?! 10-00! Подъем, славяне!') 
        elif mhmm[0] == 0 and mhmm[1] == 0:
            bot.send_message(mcid, 'Пиздуйте спать, славяне, заебали уже!')
    threading.Timer(30, morning10).start()

morning10()

#вызов всех доступных команд с проверкой на разраба
@bot.message_handler(commands=['cmd'])
def cmd(message: Message):
    if message.chat.type == 'private':
        if str(message.from_user.username) == 'koz9va' or str(message.from_user.username) == 'r4mpagelowe':
            bot.send_message(message.chat.id, 'Список команд для всех пользователей:\n'
    '/start - Приветсвие\n'
    '/help - Помощь\n'
    '/getin - Регистрация для приема/отправки анонимных сообщений\n'
    '/send - Отправка анонимных сообщений\n'
    '/reply - Команда для ответа на анонимное сообщение\n'
    '/block - Команда для блокировки анонимного отправителя\n'
    '/joke - Dolbobot пошутит\n'
    '/fact - Dolbobot поделится фактом\n'
    '/pubg - Текущий онлайн в ПУБГ\n'
    '/rates - Курсы валют\n'
    '/btc - Курс Bitcoin\n'
    '/binary - Перевод чисел из десятичной системы счисления в двоичную.\n'
    '\nСписок команд доступных только разработчикам:\n'
    '/cmd - собственно, получение этого списка\n'
    '/stop_kpop - остановка слежения за IQ\n'
    '/start_kpop - восстановление слежения за IQ\n'
    '/notify - сообщение всем юзерам, которые есть в базе\n'
    '/groups_cid - таблица чатов в которых работает бот в текущей сессии\n'
    '/send_to_group - отправка сообщения в конкретный чат')
        else:
            bot.reply_to(message, 'У вас отсутствуют достаточные полномочия для получения этой информации.')
    else:
        pass

"""
Парсер Стикеров:
@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: Message):
    id = message.sticker.file_id
    print(id)
    g = open('файл.txt', 'a', encoding='utf-8')
    g.write('\n' + id)
    g.close()
"""

"""
@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def all_message_handler(message: Message):
    if message.chat.id not in model.all_chats_id:
        model.all_chats_id.append(message.chat.id)
    else:
    pass 

@bot.message_handler(commands=['allchatsid'])
def all_chats_id(message: Message):
    if str(message.from_user.username) == 'koz9va' or str(message.from_user.username) == 'r4mpagelowe':
        acid = model.all_chats_id.split('\n')
        bot.send_message(message.chat.id, 'ID чатов, в которых используется бот:', acid)        
"""
@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def message_handler(message: Message):
    if message.chat.id not in model.kpopchats_blacklist:
        rn = random.randint(0, 8) #генерим номер строки
        t1 = message.text
        t2 = t1.split(' ')
        for word in t2:
            if str(word) in model.kpopdata:
                #print('@', message.from_user.username, '- в сообщении юзера обнаружено упоминание к-поп.', 'Тип чата:', message.chat.type) #выдача в консоль
                #print('Сообщение юзера:', t1) #выдача в консоль
                bot.send_message(message.chat.id, model.kpopans[rn]) 
                break
        if str(message.from_user.username) == 'emilichkaaaaaa':
            emili = random.randint(0, 9)
            em = random.randint(10, 13) #генерим номер строки
            if emili in model.emili_trig:
                bot.reply_to(message, model.kpopans[em])       
    if message.text == 'Бот, спс' or message.text == 'Бот, спасибо' or message.text == 'Долбобот, спс' or message.text == 'Долбобот, спасибо':
        Tsanks_massiv = ['Всегда рад помочь!', 'Рад что пригодился!', 'Обращайтесь!', 'Спасибо в карман не положешь)', 'Я просто делаю свою работу)']
        rnd = random.randint(0, 4)
        bot.reply_to(message, Tsanks_massiv[rnd]) 
    if message.text == 'Бот, подбрось монетку' or message.text == 'Бот, орел или решка':
        monetka = random.randint(0, 10)
        orel = [1, 3, 5, 7, 9]
        reshka = [2, 4, 6, 8, 10]
        if monetka in orel:
            bot.reply_to(message, 'Выпал орел!')
        elif monetka in reshka:
            bot.reply_to(message, 'Выпала решка!')
        else:
            bot.reply_to(message, 'Хмм... Монетка приземлилась на ребро...')                                    


@bot.message_handler(content_types=['sticker'])    
def sticker_handler(message: Message):
    if message.chat.id not in model.kpopchats_blacklist:
        STICKER_ID = [message.sticker.file_id] #id стикера который к нам приходит 
        for word in STICKER_ID:
            if str(word) in model.kpopstdata:
                #print('@', message.from_user.username, '- в сообщении юзера обнаружен неправедный стикер.', 'Тип чата:', message.chat.type) #выдача в консоль
                bot.send_message(message.chat.id, 'Стикер на к-поп тему... Убейте меня!')
                break    



def callbacks():
    model.updatesoap()# функция которая вызывется раз в пять минут в которая запускает все остальные функции
    model.updbtc()
    model.msg.save()   

def timers():
    for usr in range(0,len(model.msg.TooUsers)-1):
        if model.msg.TooUsers[usr][1] <= 0:
            del model.msg.TooUsers[usr]
        model.msg.TooUsers[usr][1] -= 1
if __name__ == '__main__': # проверка на прямой запуск файла, то есть если добавить его через import эти комманды не будут выполнены

    threading.Timer(300 , callbacks).start()# запуск периодических функций в отдельном потоке
#    threading.Timer(1, timers)
    bot.polling() # сам запуск бота

