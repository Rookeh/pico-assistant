import config
import os
import gc
import secrets
#import upip
import urequests
import utils
import wlan

class HomeAssistant:
    
    def __init__(self):
        self.access_token = secrets.ha_access_token
        self.areas = config.areas
        self.base_url = config.ha_instance
        wlan.connect()
        # In case your UF2 does not include urequests - this only needs to be run once.
        #upip.install("micropython-urequests")
        
    def getCameraImageBytes(self, camera_entity):             
        response = self.apiRequest("/api/camera_proxy/" + camera_entity)
        if response.status_code == 200:
            return response.content
        else:
            return None
        
    def getClimateData(self, entity_id):
        response = self.apiRequest("/api/states/" + entity_id)
        if not response.status_code == 200:
            return None
        climateJson = response.json()
        climateData = {
            "name": climateJson["attributes"]["friendly_name"],
            "current_temp": climateJson["attributes"]["current_temperature"],
            "target_temp": climateJson["attributes"]["temperature"],
            "current_preset": climateJson["attributes"]["preset_mode"],
            "supported_presets": climateJson["attributes"]["preset_modes"],
            "state": climateJson["state"]
        }
        response = None
        climateJson = None
        return climateData
    
    def setClimateTarget(self, entity_id, targetTemp):
        serviceData = {"entity_id": entity_id, "temperature": targetTemp}
        response = self.apiRequest("/api/services/climate/set_temperature", serviceData, "POST")
        statusCode = response.status_code
        response = None
        serviceData = None
        gc.collect()
        return statusCode == 200
        
    def getDevices(self, devices):
        for device in devices:
            response = self.apiRequest("/api/states/" + device["entity_id"])
            if not response.status_code == 200:
                return
            deviceJson = response.json()                        
            deviceState = deviceJson["state"]
            if "icon" in deviceJson["attributes"]:
                deviceIcon = deviceJson["attributes"]["icon"].split(":")[1]
            else:
                deviceIcon = "default"
            response = None
            gc.collect()
            yield {
                "name": deviceJson["attributes"]["friendly_name"],
                "entity_id": device["entity_id"],
                "on": deviceState in ["on", "playing"],
                "icon": deviceIcon,
                "toggle_service": device.get("toggle_service", None),
                "state": deviceState + deviceJson["attributes"].get("unit_of_measurement", "")
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
