class Motor (object):
    def __init__(self,s,name,reverse=False):
        self.name = name
        self.s = s
        if reverse:
            self.direction = 1
        else:
            self.direction = 0
        self.s.write('D,' + self.name + ',' + str(self.direction))
    def setPower(self,value):
        self.s.write('A,' + self.name + ',' + str(value))
        return int(self.s.read())
        
class Servo (object):
    def __init__(self,s,name):
        self.name = name
        self.s = s
        self.s.write('E,' + self.name);
    def setPosition(self,position):
        self.s.write('F,' + self.name + ',' + str(position))

class IrSeekerSensor (object):
    def __init__(self,s,name):
        self.s = s
        self.name = name
        self.s.write('G,' + self.name)
        
    def signalDetected(self):
        self.s.write('H,' + self.name)
        result = self.s.read()
        if result == "1":
            return True
        else:
            return False
            
    def getAngle(self):
        self.s.write('I,' + self.name)
        return float(self.s.read())
        
    def getStrength(self):
        self.s.write('J,' + self.name)
        return float(self.s.read())

class Gamepad(object):
    def __init__(self,s,name):
        self.name = name
        self.s = s

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
        self.s.write('K,' + self.name + ',' + button)
        result = self.s.read()
        if result == '1':
            return True
        else:
            return False

    def __get_axis__(self,axis):
        self.s.write('K,' + self.name + ',' + axis)
        return float(self.s.read())

    def get(self,thing):
        if thing in self.buttons:
            return self.__get_button__(self.buttons[thing])
        elif thing in self.axes:
            return self.__get_axis__(self.axes[thing])
