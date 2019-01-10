import pickle

class User:
    chatId = str()
    name = str()
    created = str()
    blocked = []
    isReady = False
    timeToSend = 0
    timeToUsr = 0
    sentToUsr = 0
    banned = False
    sentMess = 0
    def __init__(self, chtid = '', nm = '', crt = ''):
        self.chatId = chtid
        self.name = nm
        self.created = crt
    def block(self, msg):
        self.blocked.append((msg.authName, msg.author))
    def unblock(self, aunm = ''):
        for i in range(0, len(self.blocked)):
            if self.blocked[i][1] == aunm:
                del self.blocked[i]
                break

class ownmessage:
    text = str()
    author = str()
    authName = str()
    terms = True
    def __init__(self, txt = '', auth = '', authNm = '@0'):
        if len(txt) > 300:
            terms = False
        if txt == '' or txt[0] == ' ':
            terms = False
        if authNm == '@0':
            terms = False
        self.text = txt
        self.author = auth
        self.authName = authNm

class MessWork:
    Users = []
    picklFile = ''
    def __init__(self, fileL = ''):
        self.picklFile = fileL
    def start(self, usr):
        self.Users.append(usr)
    def save(self):
        with open(self.picklFile, 'wb') as output:
            pickle.dump(self.Users, output, pickle.HIGHEST_PROTOCOL)
    def f5(self):
        with open(self.picklFile, 'rb') as inpt:
            self.Users = pickle.load(inpt)

    