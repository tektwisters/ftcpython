from server import *
from activity import *
from misc import *
import traceback, sys

LOG_FILENAME = '/storage/emulated/0/ftc/log'

def log(text):
    with open(LOG_FILENAME, 'a') as f:
        f.write(text + '\n')

def log_error(e):
    for frame in traceback.extract_tb(sys.exc_info()[2]):
        fname,lineno,fn,text = frame
        t = "Error in %s on line %d" % (fname, lineno)
    log(t)
    log(repr(e))

log('\nStart of log\n')

log('Starting server...')
s = Server(1,25658)
log('Listening for clients...')
s.acceptClients()
log('Connected')

try:
    active = selected(s)
except Exception as e:
    log('Error:')
    log_error(e)

try:
    active.start()
    while running(s):
        active.loop()
except Exception as e:
    log('User code error:')
    log_error(e)
p("Stopped")
