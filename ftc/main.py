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
        
class Servo (object):
    def __init__(self,name):
        self.name = name
        tcpWrite('E,' + self.name);
    def setPosition(self,position):
        tcpWrite('F,' + self.name + ',' + str(position))

class IrSeekerSensor (object):
    def __init__(self,name):
        self.name = name
        tcpWrite('G,' + self.name)
        
    def signalDetected(self):
        tcpWrite('H,' + self.name)
        result = tcpRead()
        if result == "1":
            return True
        else:
            return False
            
    def getAngle(self):
        tcpWrite('I,' + self.name)
        return float(tcpRead())
        
    def getStrength(self):
        tcpWrite('J,' + self.name)
        return float(tcpRead())
        

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
        
class K9IrSeeker (object):
    def __init__(self):
        global MOTOR_POWER, HOLD_IR_SIGNAL_STRENGTH
        MOTOR_POWER = 0.15
        HOLD_IR_SIGNAL_STRENGTH = 0.50
        
    def start(self):
        global motorRight
        motorRight = Motor("motor_2")
        
        global motorLeft
        motorLeft = Motor("motor_1",reverse = True)
        
        global arm
        arm = Servo("servo_1")
        
        global claw
        claw = Servo("servo_6")
        
        global armPosition
        armPosition = 0.1
        
        global clawPosition
        clawPosition = 0.25
        
        global irSeeker
        irSeeker = IrSeekerSensor("ir_seeker")
    
    def loop(self):
        angle = 0.0
        strength = 0.0
        left = 0.0
        right = 0.0
        
        arm.setPosition(armPosition)
        claw.setPosition(clawPosition)
        
        if irSeeker.signalDetected():
            angle = irSeeker.getAngle()
            strength = irSeeker.getStrength
            if angle < -60:
                left = -MOTOR_POWER
                right = MOTOR_POWER
            elif angle < -5:
                left = MOTOR_POWER - 0.05
                right = MOTOR_POWER
            elif angle > 5 and angle < 60:
                left = MOTOR_POWER
                right = MOTOR_POWER - 0.05
            elif angle > 60:
                left = MOTOR_POWER
                right = -MOTOR_POWER
            elif strength < HOLD_IR_SIGNAL_STRENGTH:
                left = MOTOR_POWER
                right = MOTOR_POWER
            else:
                left = 0.0
                right = 0.0
        else:
            left = 0.0
            right = 0.0
            
        motorRight.setPower(right)
        motorLeft.setPower(left)
        
        telemetry("Text", "*** Robot Data***")
        telemetry("angle", "angle: " + str(angle))
        telemetry("strength", "sig strength: " + str(strength))
        telemetry("left tgt pwr", "left pwr: " + str(left))
        telemetry("right tgt pwr", "right pwr: " + str(right))

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
