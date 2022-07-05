ha_instance = "http://your-home-assistant-instance:8123"
areas = {
    "Living Room": [
        {
            "entity_id": "light.ceiling_light",
            "toggle_service": "light.toggle"
        }
    ],
    "Office" : [
        {
            "entity_id": "switch.desk_lamp",
            "toggle_service": "switch.toggle"
        }
    ]   
}