import config
import machine
import usocket
import ustruct
import utime

def setTime():
    ntpHost = config.ntp_host        
    query = bytearray(48)
    query[0] = 0x1B
    address = usocket.getaddrinfo(ntpHost, 123)[0][-1]
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)    
    try:
        sock.settimeout(1)
        response = sock.sendto(query, address)
        message = sock.recv(48)
    except:
        # NTP server timed out; reboot and try again
        machine.reset()
    finally:
        sock.close()
    now = ustruct.unpack("!I", message[40:44])[0]
    # Difference between NTP epoch & Unix epoch: (70*365 + 17)*86400
    delta = 2208988800
    # Flip negative/positive as we are subtracting from an offset
    offset = config.utc_offset * -1
    start = utime.mktime(config.dst_start)
    end = utime.mktime(config.dst_end)
    if config.dst_enabled and (now - delta) < start:
        # Before DST, no shifting
        delta = delta + (int(offset * 3600))
    elif config.dst_enabled and (now - delta) < end:
        # DST, subtract DST shift multiplier from offset
        delta = delta + (int((offset * 3600)) - (int(config.dst_shift * 3600)))
    else:
        # After DST or DST not observed, no shifting
        delta = delta + (int(offset * 3600))
    utc = utime.gmtime((now - delta))
    machine.RTC().datetime((utc[0], utc[1], utc[2], utc[6]+1, utc[3], utc[4], utc[5], 0))
