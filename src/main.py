from api import HomeAssistant
import config
from display import Display
from pimoroni import Button, RGBLED
import utils
import utime

class ViewMode:
    NONE = 0
    DEVICES = 1
    CAMERA = 2
    CLIMATE = 3

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
        self.viewMode = ViewMode.NONE
        self.display = Display()        
        self.display.clear()
        self.display.drawBackground("Please wait...")

    def adjustClimate(self, offset):
        climateDevice = list(self.areas.values())[self.currentArea][0]
        climateData = self.haApi.getClimateData(climateDevice["entity_id"])
        if climateData is not None:
            targetTemp = climateData["target_temp"]
            targetTemp += offset
            self.haApi.setClimateTarget(climateDevice["entity_id"], targetTemp)
            self.refreshClimate(climateDevice["entity_id"])

    def changeArea(self):
        self.viewMode = ViewMode.NONE
        areaLength = len(list(self.areas.values()))
        if self.currentArea >= 0 and self.currentArea < areaLength - 1:
            self.currentArea += 1
        else:
            self.currentArea = 0
        self.refreshArea()
              
    def refreshCamera(self, entityId):
        self.viewMode = ViewMode.CAMERA        
        self.display.clear()        
        cameraName = list(self.areas.keys())[self.currentArea]
        imgBytes = self.haApi.getCameraImageBytes(entityId)
        self.display.renderCamera(cameraName, imgBytes)
        
    def refreshClimate(self, entityId):
        self.viewMode = ViewMode.CLIMATE
        self.display.clear()
        areaName = list(self.areas.keys())[self.currentArea]
        self.display.drawBackground(areaName)
        climateData = self.haApi.getClimateData(entityId)
        if climateData is None:
            climateData = { "current_temp": "Error", "target_temp": "Error" }        
        self.display.renderClimate(climateData)
            
    def refreshArea(self):
        devices = list(self.areas.values())[self.currentArea]
        cameraPredicate = lambda device: device["entity_id"].startswith("camera.")
        climatePredicate = lambda device: device["entity_id"].startswith("climate.")
        cameraEntity = utils.firstOrDefault(devices, cameraPredicate)
        climateEntity = utils.firstOrDefault(devices, climatePredicate)
        if cameraEntity is not None:
            self.refreshCamera(cameraEntity["entity_id"])
        elif climateEntity is not None:
            self.refreshClimate(climateEntity["entity_id"])
        else:
            self.refreshDevices()        
    
    def refreshDevices(self):
        self.viewMode = ViewMode.DEVICES        
        self.display.clear()
        devices = list(utils.take(list(self.areas.values())[self.currentArea], 3))
        areaName = list(self.areas.keys())[self.currentArea]
        self.display.drawBackground(areaName)
        self.devices = list(self.haApi.getDevices(devices))
        if len(self.devices) >= 1:
            self.display.drawDevice("A", self.devices[0], self.devices[0]["on"])
        if len(self.devices) >= 2:
            self.display.drawDevice("B", self.devices[1], self.devices[1]["on"])
        if len(self.devices) == 3:
            self.display.drawDevice("X", self.devices[2], self.devices[2]["on"])
        self.display.drawChangeAreaY()
        
    def toggleDevice(self, button, deviceIndex):
        if self.devices[deviceIndex]["toggle_service"] is not None and self.haApi.toggleDevice(self.devices[deviceIndex]):
            self.devices[deviceIndex]["on"] = not self.devices[deviceIndex]["on"]
            self.display.drawDevice(button, self.devices[deviceIndex], self.devices[deviceIndex]["on"])
        
    def sleep(self):
        if not self.display.isAsleep:
            self.display.sleep()

app = App()
app.refreshArea()
lastUse = utime.ticks_ms()

while True:    
    now = utime.ticks_ms()
    if utime.ticks_diff(now, lastUse) >= 10000:
        app.sleep()
        if app.buttonA.read() or app.buttonB.read() or app.buttonX.read() or app.buttonY.read():
            lastUse = utime.ticks_ms()
            app.display.wake()
            app.refreshArea()
    else:
        if app.viewMode == ViewMode.CAMERA:
            if app.buttonY.read():                
                app.changeArea()
                lastUse = utime.ticks_ms()                
        elif app.viewMode == ViewMode.DEVICES:            
            if app.buttonA.read() and len(app.devices) >= 1:                
                app.toggleDevice("A", 0)
                lastUse = utime.ticks_ms()
            if app.buttonB.read() and len(app.devices) >= 2:                
                app.toggleDevice("B", 1)
                lastUse = utime.ticks_ms()
            if app.buttonX.read() and len(app.devices) == 3:                
                app.toggleDevice("X", 2)
                lastUse = utime.ticks_ms()
            if app.buttonY.read():                
                app.changeArea()
                lastUse = utime.ticks_ms()
        elif app.viewMode == ViewMode.CLIMATE:
            if app.buttonA.read():
                app.adjustClimate(1)
                lastUse = utime.ticks_ms()
            if app.buttonB.read():
                app.adjustClimate(-1)
                lastUse = utime.ticks_ms()
            if app.buttonX.read():
                app.cycleClimateMode()
                lastUse = utime.ticks_ms()                
    utime.sleep(0.1)
