import socket, time, android

droid = android.Android()

s = None

def p(text):
    droid.makeToast(text)
#things to begin with
def tcpConnect( HostIp, Port ):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return
    
def tcpWait ( numofclientwait, port ):
	global s2
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s2.bind(('127.0.0.1',port)) 
	s2.listen(numofclientwait) 
 
def tcpNext ( ):
		global s
		s = s2.accept()[0]
   
def tcpWrite(D):
   s.send(D + '\n')
   return 
   
def tcpRead( ):
	a = ' '
	b = ''
	while a != '\n':
		a = s.recv(1)
		b = b + a
	return b
 
def tcpClose( ):
   s.close()
   return 

class Motor (object):
    def __init__(self,name,reverse=False):
        self.name = name
        if reverse:
            self.direction = 1
        else:
            self.direction = 0
        tcpWrite('D,' + self.name + ',' + str(self.direction))
    def setPower(self,value):
        tcpWrite('A,' + self.name + ',' + str(value))
        return int(tcpRead())

def running():
    tcpWrite('C')
    result = tcpRead()
    if result[0] == '1':
        return True
    else:
        return False

def telemetry(key,data):
    tcpWrite('B,' + key + ',' + data)

#Make your own classes here
class Demo(object):
    def __init__(self):
        self.count = 0

    def start(self):
        telemetry('1','Starting...')

    def loop(self):
        telemetry('2','Looped ' + str(self.count) + ' times')
        self.count += 1


#State the currently selected class
selected = Demo()

p('Starting server...')
try:
    tcpWait(1,25658)
    p('Listening for clients...')
    tcpNext()
    p('Connected')
except Exception as e:
    p('Failed to start with Error: ' + str(e))

if type(s) != type(None):
    try:
        selected.start()
        while running():
            selected.loop()
        p('Stopped')
    except Exception as e:
        p('User code error: ' + str(e))

try:
    tcpClose()
except:
    pass
