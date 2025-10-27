from ws2812 import WS2812
import time

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

#WS2812(pin_num,led_count)
led = WS2812(18,1)
while True:
    print("fills")
    for color in COLORS:
        led.pixels_fill(color) 	# COLORE TOUTE LA BANDE DE LED EN MEME TEMPS 
        led.pixels_show()		# PREND LES COULEURS DU TUPLE ET C'EST TOUS 
        time.sleep(1)

    print("chases")
    for color in COLORS:
        led.color_chase(color, 0.55) 	# COLOR CHAQUE LED SEPAREMENT LES UNES DES AUTRES EFFET DYNAMIQUE MOUVEMENT 
                                        # PREND LES COULEURS DU TUPLE ET C'EST TOUS PAS D'AUTRES 
    print("rainbow")
    led.rainbow_cycle(0) # PREND TOUTES LES COULEURS DE L'ARC EN CIEL
    

