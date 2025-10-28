#-------- LABO_4------------
from ws2812 import WS2812
from machine import ADC,I2C
from utime import sleep
from time import ticks_ms,ticks_diff
import random 

#====== INITIALISATION========
led = WS2812(18,1)
SOUND_SENSOR = ADC(1)

#====== DEFINITION DES COULEURS======
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)

#=====Tuples des couleurs========
COLORS = (RED, YELLOW, CYAN, BLUE, PURPLE, WHITE)


# CALCUL  DU BRUIT MOYEN INITIAL
MOYENNE = 0
for i in range (1000):
    noise = SOUND_SENSOR.read_u16()/256
    MOYENNE += noise
noise = MOYENNE/1000

print("Bruit moyen initial",noise)


last_beat_time = ticks_ms()
minute_start = ticks_ms()
bpm_list = [] # creation de list pour stocker les BPM


# ===== Boucle Principal========
while True:
    
    # Lecture du son (amplitude): moyenne sur 100 mesures  
    moyenne = 0
    for i in range (100):
        noise_2 = SOUND_SENSOR.read_u16()/256
        moyenne += noise_2
    noise_2 = moyenne/100
    
    print("bruit actuel:",noise_2)
    
    current_time = ticks_ms()
    
    # Détection d’un pic sonore
    if noise_2 < noise and (current_time - last_beat_time) > 500:
        
        #===== CHANGEMENT DE COULEUR======
        print("etat changement led")
        random_color = random.choice(COLORS)
        print("color",(random_color))
        led.pixels_fill(random_color)
        led.pixels_show()
        
        
        #calcul du bpm
        interval = ticks_diff(current_time,last_beat_time)
        Bpm = 60000 / interval
        print("BPM instantané", round(Bpm,1))
        
        bpm_list.append(Bpm)  # ajouter le BPM à la liste pour moyenne
        
        
        
        last_beat_time = current_time # mise a jour du dernier battement
        
        # Calcul de la moyenne BPM toutes les 60 secondes
    if ticks_diff(current_time, minute_start) >= 60000:
        if bpm_list:  # éviter division par zéro
            avg_bpm = sum(bpm_list) / len(bpm_list)
            print("Moyenne BPM sur 1 min:", round(avg_bpm,1))
            
            # Écriture dans un fichier texte sur le Pico
            try:
                with open("bpm_log.txt", "a") as f:
                    f.write(f"{round(avg_bpm,1)} BPM\n")
                    print("ecriture reussie")
                    sleep(5)
            except Exception as e:
                print("Erreur écriture fichier:", e)
        
        # Réinitialiser la liste et le timer
        bpm_list = []
        minute_start = current_time
        
    sleep(0.01)  # lecture rapide, sans bloquer

