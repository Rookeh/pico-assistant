# Update this to point to your HA url.
ha_instance = "http://your-home-assistant-instance:8123"
# Example config, replace this with your desired layout.
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
