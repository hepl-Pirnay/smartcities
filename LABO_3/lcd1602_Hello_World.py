from LCD1602 import LCD1602
from machine import I2C,Pin
from utime import sleep
i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)
d = LCD1602(i2c, 2, 16) # label data type, number of lines and characters per line 

d.display() # enable display
sleep(1)
d.clear() # clear display
d.print('Hello ') #display characters

sleep(1)
d.setCursor(0, 1) # set display position, row and column start from 0
d.print('world ')