import logging
from telegram.ext import Updater, CommandHandler
from bs4 import BeautifulSoup
import requests

class Model():
    timer = int()
    pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text, features="html.parser")
    def updatesoap(self):
        self.pubg_site = BeautifulSoup(requests.get('https://steamcharts.com/app/578080').text)
    def getAmount(self):
        return self.pubg_site.find_all('span', class_='num')[0].contents[0]
            


model = Model()


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name)
    )
updater = Updater('APIKEY')
def pubg(bot, update):
    chat_id = bot.get_updates()[-1].message.chat_id
    bot.send_message(chat_id=chat_id, text=str(model.getAmount()))

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('pubg', pubg))

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()