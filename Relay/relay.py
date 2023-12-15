from machine import Pin

relay = Pin(26, Pin.OUT)
relay.value(1)

def on():
    relay.value(0)
    
def off():
    relay.value(1)
    
