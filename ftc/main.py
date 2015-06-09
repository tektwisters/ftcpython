from server import *
from activity import *
from misc import *

s = Server(1,25658)
s.acceptClients()

active = selected(s)

active.start()
while running(s):
    active.loop()

p("Stopped")
