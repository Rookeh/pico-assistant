import network
import ntp
import secrets
import utime

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.ssid, secrets.password)
    while not wlan.isconnected():
        utime.sleep(1)
    ntp.setTime()
