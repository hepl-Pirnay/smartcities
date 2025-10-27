from ws2812 import WS2812
from machine import ADC,I2C
from utime import sleep
import time 
import random 

led = WS2812(18,1)
SOUND_SENSOR = ADC(1)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (RED, YELLOW, CYAN, BLUE, PURPLE, WHITE)


'''utiliser time.ticks_ms ca permet de ne pas arreter le programme
ca ne fais que lire une valeur de l'horloge interne du pico '''

MOYENNE = 0
for i in range (1000):
    noise = SOUND_SENSOR.read_u16()/256
    MOYENNE += noise
noise = MOYENNE/1000
  
last_beat_time = 0

while True:
    # Lecture du son (amplitude) 
    moyenne = 0
    for i in range (100):
        noise_2 = SOUND_SENSOR.read_u16()/256
        moyenne += noise_2
    noise_2 = moyenne/100
    
    print("bruit:",(noise_2))
    
    
    # Détection d’un pic sonore
    # Si le son dépasse le seuil ET qu’au moins 200 ms se sont écoulées depuis le dernier beat :
    if noise_2 > noise and (time.ticks_ms() - last_beat_time) > 500:
        
        print("etat changement led")
        
        random_color = random.choice(COLORS)
        print("color",(random_color))
        
        # nouveau battement détecté
        led.pixels_fill(random_color)
        led.pixels_show()
        last_beat_time = time.ticks_ms()
        
        
        noise = noise_2
    
    sleep(0.01)  # lecture rapide, sans bloquer
