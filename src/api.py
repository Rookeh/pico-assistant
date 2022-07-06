import config
import gc
import secrets
import time
#import upip
import urequests
import wlan

class HomeAssistant:
    
    def __init__(self):
        self.access_token = secrets.ha_access_token
        self.areas = config.areas
        self.base_url = config.ha_instance
        wlan.connect()
        # In case your UF2 does not include urequests - this only needs to be run once.
        #upip.install("micropython-urequests")
        
    def getDevices(self, area):
        for device in area:            
            response = self.apiRequest("/api/states/" + device["entity_id"])
            if not response.status_code == 200:
                return
            deviceJson = response.json()            
            deviceName = deviceJson["attributes"]["friendly_name"]            
            deviceState = deviceJson["state"]
            if "icon" in deviceJson["attributes"]:
                deviceIcon = deviceJson["attributes"]["icon"].split(":")[1]
            else:
                deviceIcon = "default"
            response = None
            gc.collect()
            yield {
                "name": deviceName,
                "entity_id": device["entity_id"],
                "on": deviceState not in ["off", "unknown", "unavailable"],
                "icon": deviceIcon,
                "toggle_service": device["toggle_service"]
            }
            
    def toggleDevice(self, device):
        serviceData = {"entity_id": device["entity_id"]}
        response = self.apiRequest("/api/services/" + device["toggle_service"].replace(".", "/"), serviceData, "POST")
        statusCode = response.status_code
        response = None
        serviceData = None
        gc.collect()
        return statusCode == 200
        
    def apiRequest(self, endpoint, json=None, verb="GET"):        
        url = self.base_url + endpoint
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "content-type": "application/json"
        }
        response = None        
        if verb == "GET":     
            response = urequests.get(url, headers=headers)
        else:
            response = urequests.post(url, headers=headers, json=json)            
        return response
