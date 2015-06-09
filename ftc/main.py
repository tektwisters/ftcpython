import socket, time, android, numpy

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

class Gamepad(object):
    def __init__(self,name):
        self.name = name

        self.buttons = {
            'a': 'a',
            'b': 'b',
            'x': 'x',
            'y': 'y',
            'dpad_up': 'du',
            'dpad_down': 'dd',
            'dpad_left': 'dl',
            'dpad_right': 'dr',
            'left_bumper': 'lb',
            'right_bumper': 'rb'
            }

        self.axes = {
            'right_stick_x': 'rx',
            'right_stick_y': 'ry',
            'left_stick_x' : 'lx',
            'left_stick_y' : 'ly',
            'left_trigger' : 'lt',
            'right_trigger': 'rt'
            }

        

    def __get_button__(self,button):
        tcpWrite('K,' + self.name + ',' + button)
        result = tcpRead()
        if result == '1':
            return True
        else:
            return False

    def __get_axis__(self,axis):
        tcpWrite('K,' + self.name + ',' + axis)
        return float(tcpRead())

    def get(self,thing):
        if thing in self.buttons:
            return self.__get_button__(self.buttons[thing])
        elif thing in self.axes:
            return self.__get_axis__(self.axes[thing])

gamepad1 = Gamepad('1')
gamepad2 = Gamepad('2')

def running():
    tcpWrite('C')
    result = tcpRead()
    if result[0] == '1':
        return True
    else:
        return False

def telemetry(key,data):
    tcpWrite('B,' + key + ',' + data)

def clip(value,minValue,maxValue):
    return max(min(value, maxValue), minValue)

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

class K9TankDrive (object):
    def __init__(self):
        global ARM_MIN_RANGE, ARM_MAX_RANGE, CLAW_MIN_RANGE, CLAW_MAX_RANGE
        ARM_MIN_RANGE = 0.20
        ARM_MAX_RANGE = 0.90
        CLAW_MIN_RANGE = 0.20
        CLAW_MAX_RANGE = 0.7

        global armDelta
        armDelta = 0.1

        global clawDelta
        clawDelta = 0.1

    def start(self):
        global motorRight
        motorRight = Motor("motor_2")
        global motorLeft
        motorLeft = Motor("motor_1",reverse=True)
        global arm
        arm = Servo("servo_1")
        global claw
        claw = Servo("servo_6")
        global armPosition
        armPosition = 0.2
        global clawPosition
        clawPosition = 0.2

    def scaleInput(dVal):
        scaleArray = [0.0,0.05, 0.09, 0.10, 0.12, 0.15, 0.18, 0.24,
                      0.30, 0.36, 0.43, 0.50, 0.60, 0.72, 0.85, 1.0, 1.0]

        index = int(dVal*16.0)
        if index < 0:
            index = -index
        elif index > 16:
            index = 16

        dScale = 0.0
        if dVal < 0:
            dScale = -scaleArray[index]
        else:
            dScale = scaleArray[index]

        return dScale

    def loop(self):
        left = -gamepad1.get("left_stick_y")
        right = -gamepad1.get("right_stick_y")

        right = clip(right,-1,1)
        left = clip(left,-1,1)

        right = self.scaleInput(right)
        left = self.scaleInput(left)

        motorRight.setPower(right)
        motorLeft.setPower(left)

        if gamepad1.get('a'):
            armPosition += armDelta

        if gamepad1.get('y'):
            armPosition -= armDelta

        if gamepad1.get('left_bumper'):
            clawPosition += clawDelta

        if gamepad1.get('left_trigger') > 0.25:
            clawPosition -= clawDelta

        if gamepad1.get('x'):
            clawPosition += clawDelta

        if gamepad1.get('b'):
            clawPosition -= clawDelta

        armPosition = clip(armPosition, ARM_MAX_RANGE, ARM_MAX_RANGE)
        clawPosition = clip(clawPosition, CLAW_MIN_RANGE, CLAW_MAX_RANGE)

        arm.setPosition(armPosition)
        claw.setPosition(clawPosition)

        telemetry("Text", "*** Robot Data***")
        telemetry("arm", "arm: " + str(armPosition))
        telemetry("claw", "claw: " + str(clawPosition))
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
