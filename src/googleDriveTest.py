#!/usr/bin/env micropython
# -*- coding: utf-8 -*-

import network
from machine import Pin, Timer, I2C, ADC
import camera
import machine
import time
import uasyncio as asyncio
import ubinascii
import gc
import usocket
import json
import urequests

__author__ = "Marciel Barros Pereira"
__credits__ = ["Marciel Barros Pereira"]
__maintainer__ = "Marciel Barros Pereira"
__email__ = "marcielbp@gmail.com"




sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
try:
    sta_if.disconnect()
except:
    pass
redes = sta_if.scan()

knownSsid = [b'put',b'your',b'known',b'essid-here']
knownPasswd = [b'put',b'known-essid',b'passwords',b'here']

ssidmode = False
for i in range (0,len(knownSsid)):
    for j in range (0,len(redes)):
        print("Compare {} with {}".format(knownSsid[i],redes[j][0]))
        if (knownSsid[i]==redes[j][0]):
            print("Connecting to {}".format(knownSsid[i]))
            sta_if.connect(knownSsid[i],knownPasswd[i])
            while sta_if.isconnected() == False:
                pass
            print('Connection successful')
            ssid = knownSsid[i]
            ssidmode = True
            print(sta_if.ifconfig())
            break
# check framesize modes in https://github.com/shariltumin/esp32-cam-micropython
camera.init()
camera.framesize(5)
buf = camera.capture()
camera.deinit()

# there is no need to save right now, but, if you want to save file, use followigng code
# newFile = open("ESP32-CAM.jpg", "wb")
# newFile.write(buf)
# newFile.close()

# Create base64 string from image bytearray
bufBase64 = ubinascii.b2a_base64(buf)

# gather some free memory
gc.collect()

myScriptID = 'putYourScriptIdHere'
url = 'https://script.google.com/macros/s/'+myScriptID+'/exec'
myScript = '/macros/s/'+myScriptID+'/exec'

myFilename = "filename=ESP32-CAM.jpg&mimetype=image/jpeg&data="
#myFilename = "imgBase64="
myDomain = "script.google.com"

# below lines were adapted from urequests lib

a = bufBase64.decode()
data = myFilename + a
method = "POST"
try:
    proto, dummy, host, path = url.split("/", 3)
except ValueError:
    proto, dummy, host = url.split("/", 2)
    path = ""
if proto == "http:":
    port = 80
elif proto == "https:":
    import ussl
    port = 443
else:
    raise ValueError("Unsupported protocol: " + proto)

if ":" in host:
    host, port = host.split(":", 1)
    port = int(port)

ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
ai = ai[0]

s = usocket.socket(ai[0], ai[1], ai[2])

s.connect(ai[-1])
if proto == "https:":
    s = ussl.wrap_socket(s, server_hostname=host)
s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))

s.write(b"Host: %s\r\n" % host)
# Iterate over keys to avoid tuple alloc
s.write(b"Content-Length: %d\r\n" % len(data))
s.write(b"Content-Type: application/x-www-form-urlencoded\r\n")
s.write(b"\r\n")

s.write(data)

l = s.readline()

l = l.split(None, 2)
status = int(l[1])
reason = ""
if len(l) > 2:
    reason = l[2].rstrip()
while True:
    l = s.readline()
    if not l or l == b"\r\n":
        break
    if l.startswith(b"Transfer-Encoding:"):
        if b"chunked" in l:
            raise ValueError("Unsupported " + l)
    elif l.startswith(b"Location:") and not 200 <= status <= 299:
        raise NotImplementedError("Redirects not yet supported")
