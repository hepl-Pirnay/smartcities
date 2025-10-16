from LCD1602 import LCD1602
from dht import DHT11
from machine import I2C,Pin,ADC,PWM
from utime import sleep

i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)
d = LCD1602(i2c, 2, 16)
d.display()
sensor = DHT11(Pin(18))
buzzer = PWM(Pin(16))

while True:
    sensor.measure()
    temp=sensor.temperature()
    humid=sensor.humidity()
    d.clear()
    d.setCursor(0,0)
    d.print("Temp:"+str(temp))
    d.setCursor(0,1)
    d.print("Humid:"+str(humid))
    sleep(1)
    
    if temp >30 or humid <30:
        buzzer.freq(1000)
        buzzer.duty_u16(1000)
    else:
        buzzer.duty_u16(0)#close