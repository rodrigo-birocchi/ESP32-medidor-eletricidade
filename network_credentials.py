import network


SSID = ""
PASS = ""

print("Starting network...")

sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print("Connecting to network")
    sta.active(True)
    sta.connect(SSID, PASS)
    
    while not sta.isconnected():
        pass
    
    print("Network config: ", sta.ifconfig())
else:
    print("Already connected")
    print("Network config: ", sta.ifconfig())