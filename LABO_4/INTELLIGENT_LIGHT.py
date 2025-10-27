from ws2812 import WS2812
from machine import I2C,Pin,ADC
from utime import sleep

led = WS2812(18,1)
LIGHT_SENSOR = ADC(0)
SOUND_SENSOR = ADC(1)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)

while True:
    average = 0
    light = LIGHT_SENSOR.read_u16()/256
    for i in range (1000):
        noise = SOUND_SENSOR.read_u16()/256
        average += noise
    noise = average/1000
    print ("bruit:",(noise))
    print("light:",(light))
    if light < 80:
        led.pixels_fill(WHITE)
        led.pixels_show()
        sleep(0.2)
    else:
        if noise < 25:
            led.pixels_fill(GREEN)
            led.pixels_show()
            sleep(1)
        if noise >= 25 and noise < 50:
            led.pixels_fill(YELLOW)
            led.pixels_show()
            sleep(1)
        if noise >= 50:
            led.pixels_fill(RED)
            led.pixels_show()
            sleep(1)