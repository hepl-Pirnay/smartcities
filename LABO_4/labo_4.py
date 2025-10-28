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


# ======CALCUL  DU BRUIT MOYEN INITIAL=====================
def calcul_bruit_initial(n=1000):
    total = 0
    for i in range(n):
        total += SOUND_SENSOR.read_u16()/256
    return total / n

noise_initial = calcul_bruit_initial()
print("Bruit moyen initial",noise_initial)

#========= Fonction =============================
def lire_son(mesures=100):
    """Lecture moyenne du son sur 'x(mesures)' valeurs"""
    total = 0
    for _ in range(mesures):
        total += SOUND_SENSOR.read_u16() / 256
    return total / mesures

def changer_couleur_led():
    """Choisit une couleur aléatoire et met à jour la LED"""
    couleur = random.choice(COLORS)
    led.pixels_fill(couleur)
    led.pixels_show()
    print("Changement couleur:", couleur)
    
def calculer_bpm(current_time, last_time, bpm_list):
    """Calcul du BPM instantané et ajout à la liste"""
    interval = ticks_diff(current_time, last_time)
    if interval > 0:
        bpm = 60000 / interval
        bpm_list.append(bpm)
        print("BPM instantané:", round(bpm,1))
    return bpm_list

def enregistrer_bpm(bpm_list, fichier="bpm_log.txt"):
    """Calcul de la moyenne BPM et écriture dans le fichier"""
    if bpm_list:
        avg_bpm = sum(bpm_list) / len(bpm_list)
        print("Moyenne BPM sur 1 min:", round(avg_bpm,1))
        try:
            with open(fichier, "a") as f:
                f.write(f"{round(avg_bpm,1)} BPM\n")
                print("Écriture réussie dans", fichier)
        except Exception as e:
            print("Erreur écriture fichier:", e)
    bpm_list.clear()  # réinitialiser la liste après écriture

#==========Variables===================
last_beat_time = ticks_ms()
minute_start = ticks_ms()
bpm_list = [] # creation de list pour stocker les BPM


# ===== Boucle Principal========
while True:
    
    current_noise = lire_son()
    print("Bruit actuel:", current_noise)
        
    current_time = ticks_ms()
    
    # Détection d’un pic sonore
    if current_noise < noise_initial and ticks_diff(current_time,last_beat_time) > 500:
        print("Pic sonore detecté")
        changer_couleur_led()
        bpm_list = calculer_bpm(current_time,last_beat_time,bpm_list)
        last_beat_time = current_time 
        
        
        # Calcul de la moyenne BPM toutes les 60 secondes
    if ticks_diff(current_time, minute_start) >= 60000:
        enregistrer_bpm(bpm_list)
        sleep(5)
        minute_start = current_time
        
        
    sleep(0.01)  # lecture rapide, sans bloquer

