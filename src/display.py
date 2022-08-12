import icons
import gc
import jpegdec
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import utils
import utime

class Display:

  def __init__(self):
      gc.enable()
      self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=0)
      self.width, self.height = self.display.get_bounds()    
      self.eraserPen = self.display.create_pen(0, 0, 0)
      self.inactivePen = self.display.create_pen(68, 115, 158)
      self.activePen = self.display.create_pen(253, 216, 53)
      self.whitePen = self.display.create_pen(255, 255, 255)
      self.display.set_backlight(0.5)
      
  def getHeaderFontPen(self):
      now = utime.localtime(utime.time())
      if now[3] >= 7 and now[3] <= 20:
          return self.display.create_pen(225, 225, 225)          
      else:
          return self.display.create_pen(33, 33, 33)
    
  def getFontPen(self):
      now = utime.localtime(utime.time())
      if now[3] >= 7 and now[3] <= 20:
          return self.display.create_pen(33, 33, 33)
      else:
          return self.display.create_pen(225, 225, 225)
        
  def getBgPen(self):
      now = utime.localtime(utime.time())      
      if now[3] >= 7 and now[3] <= 20:
          return self.display.create_pen(250, 250, 250)
      else:
          return self.display.create_pen(17, 17, 17)
    
  def getHeaderPen(self):
      now = utime.localtime(utime.time())      
      if now[3] >= 7 and now[3] <= 20:
          return self.display.create_pen(3, 169, 244)
      else:
          return self.display.create_pen(40, 74, 89)
        
  def drawIcon(self, x, y, iconKey, isActive):      
      if iconKey in icons.icons:
          icon = icons.icons[iconKey]
      else:
          icon = icons.icons["default"]
      transformed = list(self.transformIcon(x, y, icon))      
      if isActive:
          self.display.set_pen(self.activePen)
      else:
          self.display.set_pen(self.inactivePen)
      self.display.polygon(transformed)
      self.display.update()
      icon = None
      transformed = None
      gc.collect()      

  def transformIcon(self, xOffset, yOffset, icon):
      for (x, y) in icon:
          yield (int(x + xOffset), int(y + yOffset))

  def clear(self):
      self.isAsleep = True
      self.display.set_pen(self.eraserPen)
      self.display.clear()
      self.display.update()
  
  def drawBackground(self, areaName):
      timeString = utils.getTimeString()
      self.isAsleep = False
      self.display.set_pen(self.getHeaderPen())
      self.display.rectangle(0, 0, self.width, 50)
      self.display.set_pen(self.getBgPen())
      self.display.rectangle(0, 50, self.width, self.height - 50)
      self.display.set_pen(self.whitePen)
      self.display.text(areaName, self.getCentreTextPosition(areaName), 20, 240, 2)
      self.display.text(timeString, self.width - self.display.measure_text(timeString, 2) - 10, 20, 240, 2)
      self.display.update()

  def drawDevice(self, button, device, on):
      nameWidth = self.display.measure_text(device["name"], 2)
      stateWidth = self.display.measure_text(device["state"], 2)
      if button == "A":
          iX = nameWidth / 2 - 20
          iY = 50
          tX = 1
          tY = 80
          sX = 1
          sY = 95
      elif button == "B":
          iX = nameWidth / 2 - 20
          iY = self.height - 60
          tX = 1
          tY = self.height - 30
          sX = 1
          sY = self.height - 15
      else:
          iX = self.width - (nameWidth / 2)
          iY = 50
          tX = self.width - nameWidth
          tY = 80
          sX = self.width - stateWidth
          sY = 95
      self.drawIcon(iX, iY, device["icon"], on)
      self.display.set_pen(self.getFontPen())
      self.display.text(device["name"], tX, tY, 240, 2)
      self.display.text(device["state"], sX, sY, 240, 2)
      self.display.update()  
      
  def drawChangeAreaY(self):
      self.isAsleep = False      
      self.display.set_pen(self.getFontPen())
      self.display.text("Next Area", self.width - self.display.measure_text("Next Area", 2), self.height - 20, 240, 2)
      self.display.update()
      
  def renderCamera(self, areaName, imgBytes):
      self.isAsleep = False
      timeString = utils.getTimeString()
      if imgBytes is not None:
          decoder = jpegdec.JPEG(self.display)      
          decoder.open_RAM(memoryview(imgBytes))
          decoder.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
      else:
          e = "Failed to get camera image"
          self.display.set_pen(self.whitePen)
          self.display.text(e, self.getCentreTextPosition(e), 100, 240, 2)
          self.display.update()
      self.display.set_pen(self.whitePen)
      self.display.text(areaName, self.getCentreTextPosition(areaName), 200, 240, 2)
      self.display.text(timeString, self.width - self.display.measure_text(timeString, 2) - 10, 200, 240, 2)      
      self.display.update()  

  def getCentreTextPosition(self, text):
      return int(self.width - self.width / 2 - int(self.display.measure_text(text, 2) / 2))    
            
  def sleep(self):
      self.display.set_backlight(0)      
      self.clear()
      
  def wake(self):
      self.display.set_backlight(0.5)
      self.clear()
