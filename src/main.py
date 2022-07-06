from api import HomeAssistant
import config
from display import Display
from pimoroni import Button, RGBLED
import utime

class App:
    
    def __init__(self):
        self.haApi = HomeAssistant()
        self.areas = config.areas
        self.buttonA = Button(12)
        self.buttonB = Button(13)
        self.buttonX = Button(14)
        self.buttonY = Button(15)
        self.led = RGBLED(6,7,8)
        self.led.set_rgb(0,0,0)
        self.currentArea = 0
        self.devices = None
        self.display = Display()        
        self.display.clear()
        self.display.drawBackground("Please wait...")

    def changeArea(self):
        areaLength = len(list(self.areas.values()))
        if self.currentArea >= 0 and self.currentArea < areaLength - 1:
            self.currentArea += 1
        else:
            self.currentArea = 0
    
    def refreshDevices(self):
        self.display.clear()
        area = list(self.areas.values())[self.currentArea]
        areaName = list(self.areas.keys())[self.currentArea]
        self.display.drawBackground(areaName)
        self.devices = list(self.haApi.getDevices(area))[0:3]
        if len(self.devices) >= 1:
            self.display.drawDevice("A", self.devices[0], self.devices[0]["on"])
        if len(self.devices) >= 2:
            self.display.drawDevice("B", self.devices[1], self.devices[1]["on"])
        if len(self.devices) == 3:
            self.display.drawDevice("X", self.devices[2], self.devices[2]["on"])
        self.display.drawChangeAreaY()
        
    def toggleDevice(self, button, deviceIndex):
        if self.haApi.toggleDevice(self.devices[deviceIndex]):
            self.devices[deviceIndex]["on"] = not self.devices[deviceIndex]["on"]
            self.display.drawDevice(button, self.devices[deviceIndex], self.devices[deviceIndex]["on"])
        
    def sleep(self):
        if not self.display.isAsleep:
            self.display.sleep()

app = App()
app.refreshDevices()
lastUse = utime.ticks_ms()

while True:    
    now = utime.ticks_ms()
    if utime.ticks_diff(now, lastUse) >= 10000:
        app.sleep()
        if app.buttonA.read() or app.buttonB.read() or app.buttonX.read() or app.buttonY.read():
            lastUse = utime.ticks_ms()
            app.refreshDevices()
    else:
        if app.buttonA.read() and len(app.devices) >= 1:
            lastUse = utime.ticks_ms()
            app.toggleDevice("A", 0)
        if app.buttonB.read() and len(app.devices) >= 2:
            lastUse = utime.ticks_ms()
            app.toggleDevice("B", 1)
        if app.buttonX.read() and len(app.devices) == 3:
            lastUse = utime.ticks_ms()
            app.toggleDevice("X", 2)
        if app.buttonY.read():
            lastUse = utime.ticks_ms()
            app.changeArea()
            app.refreshDevices()
    
    utime.sleep(0.1)
