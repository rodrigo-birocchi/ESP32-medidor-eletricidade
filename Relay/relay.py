from machine import Pin

relay = Pin(26, Pin.OUT)

def on():
    relay.value(0)
    
def off():
    relay.value(1)
    
