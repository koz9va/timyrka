import pickle

class ownmessage:
    text = str()
    author = str()
    authName = str()
    To = str()
    def __init__(self, txt = '', auth = '', authNm = '@0'):
        self.text = txt
        self.author = auth
        self.authName = authNm
class User:
    chatId = str()
    name = str()
    blocked = []
    isReady = False
    timeToSend = 0
    timeToUsr = 0
    sentUsrs = []
    sentToUsr = 0
    last = str()
    lastName = str()
    lastM = ownmessage()
    banned = False
    sentMess = 0
    def __init__(self, chtid = '', nm = ''):
        self.chatId = chtid
        self.name = '@'+nm
    def block(self, msg):
        self.blocked.append((msg.authName, msg.author))
    def unblock(self, aunm = ''):
        for i in range(0, len(self.blocked)):
            if self.blocked[i][1] == aunm:
                del self.blocked[i]
                break
class MessWork:
    Users = []
    TooUsers = []
    picklFile = ''
    def __init__(self, fileL = ''):
        self.picklFile = fileL
        try:
            self.f5()
        except:
            print('free file')
            self.save()
    def start(self, usr):
        self.Users.append(usr)
        self.save()
    def save(self):
        with open(self.picklFile, 'wb') as output:
            pickle.dump(self.Users, output, pickle.HIGHEST_PROTOCOL)
    def f5(self):
        with open(self.picklFile, 'rb') as inpt:
            self.Users = pickle.load(inpt)

    