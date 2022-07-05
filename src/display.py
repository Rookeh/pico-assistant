import icons
import gc
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
from pimoroni import Button
import time

class Display:

  def __init__(self):
      gc.enable()
      self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=0)
      self.width, self.height = self.display.get_bounds()    
      self.eraserPen = self.display.create_pen(0, 0, 0)
      self.inactivePen = self.display.create_pen(68, 115, 158)
      self.activePen = self.display.create_pen(253, 216, 53)
    
  def getFontPen(self):
      now = time.localtime(time.time())
      if now[3] >= 7 and now[3] <= 21:
          return self.display.create_pen(33, 33, 33)
      else:
          return self.display.create_pen(225, 225, 225)
        
  def getBgPen(self):
      now = time.localtime(time.time())      
      if now[3] >= 7 and now[3] <= 21:
          return self.display.create_pen(250, 250, 250)
      else:
          return self.display.create_pen(17, 17, 17)
    
  def getHeaderPen(self):
      now = time.localtime(time.time())      
      if now[3] >= 7 and now[3] <= 21:
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
      self.isCleared = True
      self.display.set_pen(self.eraserPen)
      self.display.clear()
      self.display.update()
  
  def drawBackground(self, areaName):
      self.isCleared = False
      self.display.set_pen(self.getHeaderPen())
      self.display.rectangle(0, 0, self.width, 50)
      self.display.set_pen(self.getFontPen())
      self.display.text(areaName, int(self.width - self.width / 2 - int(self.display.measure_text(areaName, 2) / 2)), 20, 240, 2)
      self.display.set_pen(self.getBgPen())
      self.display.rectangle(0, 50, self.width, self.height - 50)
      self.display.update()

  def drawDevice(self, button, device, on):
      textWidth = self.display.measure_text(device["name"], 2)
      if button == "A":
          iX = textWidth / 2 - 20
          iY = 62
          tX = 0
          tY = 100
      elif button == "B":
          iX = textWidth / 2 - 20
          iY = self.height - 60
          tX = 0
          tY = self.height - 20
      else:
          iX = self.width - (textWidth / 2)
          iY = 62
          tX = self.width - textWidth
          tY = 100
      self.drawIcon(iX, iY, device["icon"], on)
      self.display.set_pen(self.getFontPen())
      self.display.text(device["name"], tX, tY, 240, 2)
      self.display.update()  
      
  def drawChangeAreaY(self):
      self.isCleared = False      
      self.display.set_pen(self.getFontPen())
      self.display.text("Next Area", self.width - self.display.measure_text("Next Area", 2), self.height - 20, 240, 2)
      self.display.update()
