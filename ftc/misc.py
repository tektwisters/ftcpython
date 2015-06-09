import android

droid = android.Android()

def p(text):
    droid.makeToast(text)

def running(s):
    s.write('C')
    result = s.read()
    if result[0] == '1':
        return True
    else:
        return False

def telemetry(s,key,data):
    s.write('B,' + key + ',' + data)

def clip(value,minValue,maxValue):
    return max(min(value, maxValue), minValue)
