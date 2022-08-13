# NTP Config:
# NTP time server:
ntp_host = "pool.ntp.org"
# Your timezone's offset from UTC in hours:
# (e.g. GMT = 0.0, EST = -5.0, CET = 1.0, NPT = 5.75, etc.)
utc_offset = 0.0
# True if DST is observed by your timezone, otherwise False.
dst_enabled = True
# Daylight savings time start/end dates:
dst_start = (2022, 03, 27, 1, 0, 0, 0, 0, 0)
dst_end = (2022, 10, 30, 2, 0, 0, 0, 0, 0)
# Number of hours shifted during DST:
dst_shift = 1.0

# Home Assistant config:
# Update this to point to your HA url.
ha_instance = "http://your-home-assistant-instance:8123"
# Example config, replace this with your desired layout.
areas = {
    "Living Room": [
        {
            "entity_id": "light.ceiling_light",
            "toggle_service": "light.toggle"
        },
        {
            "entity_id": "media_player.living_room_tv",
            "toggle_service": "media_player.toggle"
        }        
    ],
    "Office" : [
        {
            "entity_id": "switch.desk_lamp",
            "toggle_service": "switch.toggle"
        }
    ],
    "Hallway": [
        {
            "entity_id": "climate.nest_thermostat"
        }
    ],
    "Outside" : [
        {
            "entity_id": "camera.outside"
        }
    ]
}
