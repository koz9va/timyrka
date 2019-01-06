import random
import logging
import time, threading
from telegram.ext import Updater, CommandHandler
from bs4 import BeautifulSoup
import requests

class Model():
    timer = int()
    pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text, features="html.parser").find_all('span', class_='num')[0].contents[0]
    helloFile = open('hello.txt', 'r')
    hellodata = helloFile.readlines()
    helloFile.close()
    def updatesoap(self):
        self.pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text, features="html.parser").find_all('span', class_='num')[0].contents[0]
    def getAmount(self):
        return self.pubg_site
            

model = Model()

def hello(bot, update):
    rn = random.randint(0, len(model.hellodata))
    update.message.reply_text(
        'Привет, {}!'.format(update.message.from_user.first_name)
    )
    bot.sendMessage(chat_id=update.message.chat_id, text=model.hellodata[rn])
updater = Updater('771027063:AAHjnTSc5uH5BapuPAHsHwuKiN7VaQludzc')
def pubg(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Текущий онлайн в PUBG: ' + str(model.getAmount()))

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('pubg', pubg))
def callbacks():
    model.updatesoap()
    threading.Timer(300 , callbacks).start()
if __name__ == '__main__':
    callbacks()
    updater.start_polling()
    updater.idle()

