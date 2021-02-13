### This file uses a button to act as a detection, but is mainly to test the OLED screen.


import utime
from machine import Pin, I2C
from ssd1306 import SSD1306
import framebuf
import machine
import math

#debugled = machine.Pin(25, machine.Pin.OUT)
#debugled.toggle()
#utime.sleep(1)
#debugled.toggle()
#utime.sleep(1)
#debugled.toggle()
#utime.sleep(1)
#debugled.toggle()
#print("Debug complete")

i2c = I2C(0)

oled = SSD1306(128, 64, i2c)

sensor_temp = machine.ADC(4)
conversion_factor = 3.3/ (65535)

buttonsupply = machine.Pin(14, machine.Pin.OUT)
buttonsupply.value(1)
buttonread = machine.Pin(13, machine.Pin.IN)

headerart = [
        "00000000000000000000000000000000",
        "01111110000111110000011111111110",
        "01000011100111111100011111111110",
        "01011101110111111110011111111110",
        "01011101110111111111011111111110",
        "01000011111111111111011111111110",
        "01011111111111111111011111111110",
        "01011111110111111111011111111110",
        "01011111110111111111011111111110",
        "01111111100111111111011111111110",
        "01111110000111111111011111111110",
        "01110000000111111111011111111110",
        "01110000000111111110011111111110",
        "01110000000111111100001111111100",
        "01110000000111110000000011110000",
        "0000000000000000000000000000000"
    ]

upart = [
        "0000000000000000",
        "0000001111000000",
        "0000011111100000",
        "0000111111110000",
        "0001111111111000",
        "0011111111111100",
        "0111111111111110",
        "0000000000000000"
    ]

downart = [
        "0000000000000000",
        "0111111111111110",
        "0011111111111100",
        "0001111111111000",
        "0000111111110000",
        "0000011111100000",
        "0000001111000000",
        "0000000000000000"
    ]

nochangeart = [
        "0000000000000000",
        "0111111111111110",
        "0111111111111110",
        "0000000000000000",
        "0000000000000000",
        "0111111111111110",
        "0111111111111110",
        "0000000000000000"
    ]

oled.fill(0)
oled.art_list(headerart,1,0,debug=False)
oled.vline(34,0,16,1)
oled.vline(35,0,16,1)
oled.vline(110,0,16,1)
oled.vline(111,0,16,1)

oled.rect(0,16,128,48,1)

oled.show()

previous_temperature = 0
temperature = 0
powered = True
power_on_time = 0
while True:
    if buttonread.value() > 0:
        powered = True
        power_on_time = 0
    
    if powered == True:
        if oled.is_on == False:
            oled.poweron()
        else:
            power_on_time = power_on_time + 5
            
        oled.fill_rect(112,0,16,15,0)
        reading = sensor_temp.read_u16() * conversion_factor 
        temperature = math.trunc(27 - (reading - 0.706)/0.001721)
        if previous_temperature > temperature:
            oled.art_list(downart,112,8)
        elif previous_temperature < temperature:
            oled.art_list(upart,112,8)
        else:
            oled.art_list(nochangeart,112,8)
        
        previous_temperature = temperature

        oled.text(str(temperature),112,0)
        oled.show()
        utime.sleep(5)
    
    if power_on_time > 30:
        oled.poweroff()
        powered = False
        power_on_time = 0
        
    utime.sleep(0.1)
