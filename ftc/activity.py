from hardware import *
from misc import *


#Make your own classes here
class Demo(object):
    def __init__(self,server):
        global s
        s = server
        self.count = 0

    def start(self):
        telemetry(s,'1','Starting...')

    def loop(self):
        telemetry(s,'2','Looped ' + str(self.count) + ' times')
        self.count += 1
        
class K9IrSeeker (object):
    def __init__(self,server):
        global s
        s = server
        global MOTOR_POWER, HOLD_IR_SIGNAL_STRENGTH
        MOTOR_POWER = 0.15
        HOLD_IR_SIGNAL_STRENGTH = 0.50
        
    def start(self):
        global motorRight
        motorRight = Motor(s,"motor_2")
        
        global motorLeft
        motorLeft = Motor(s,"motor_1",reverse = True)
        
        global arm
        arm = Servo(s,"servo_1")
        
        global claw
        claw = Servo(s,"servo_6")
        
        global armPosition
        armPosition = 0.1
        
        global clawPosition
        clawPosition = 0.25
        
        global irSeeker
        irSeeker = IrSeekerSensor(s,"ir_seeker")
    
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
    def __init__(self,server):
        global s
        s = server
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
        motorRight = Motor(s,"motor_2")
        global motorLeft
        motorLeft = Motor(s,"motor_1",reverse=True)
        global arm
        arm = Servo(s,"servo_1")
        global claw
        claw = Servo(s,"servo_6")
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

        telemetry(s,"Text", "*** Robot Data***")
        telemetry(s,"arm", "arm: " + str(armPosition))
        telemetry(s,"claw", "claw: " + str(clawPosition))
        telemetry(s,"left tgt pwr", "left pwr: " + str(left))
        telemetry(s,"right tgt pwr", "right pwr: " + str(right))
        
        

        
        
        

#State the currently selected class
selected = Demo
