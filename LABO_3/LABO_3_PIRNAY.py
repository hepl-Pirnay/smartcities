'''Programme de l'exercice 3'''

'''---Librairie setup-----'''
from LCD1602 import LCD1602 		#importation de la fonction LCD1602 depuis la librairie LCD1602. 
from dht import DHT11  				# importation de la fonction DHT11 depuis la librairie dht.
from machine import I2C,Pin,ADC,PWM # importation des fonctions pin,adc,pwm,i2c depuis la librairie machine.
from utime import sleep 			#importation de la fonction sleep depuis la librairie time.


'''---Hardware setup----'''
pot = ADC(0)				#potentiometre raccorder sur ADC0 soit A0 sur la carte.
led = PWM(Pin(20))			# led raccorder sur Pin 20 soit D20 sur la carte.
led.freq(1000)
sensor = DHT11(Pin(18)) 	#Initialise le capteur DHT11 connecté sur D18 de la carte.
buzzer = PWM(Pin(16))   	#Crée un signal PWM (modulation de largeur d’impulsion) sur la broche 16.

i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000) # Initialise le bus I²C numéro 1.
                                                 # scl (clock) sur la broche GPIO7 et sda (data) sur GPIO6. Vitesse du bus : 400 kHz.
d = LCD1602(i2c, 2, 16) 						 #Crée un objet d pour piloter un écran LCD 16 colonnes × 2 lignes via I²C.
d.display() 									 # active l’affichage (allume l’écran).

'''------Definition de la fonction led_dimmer-----'''
def led_dimmer(): 
    # petite passe montée/descente rapide
    step = 4000  # le pas entre chaque incrementation
    delay = 0.005 # le delay d'attente ou le system ce met en pause 
    # montée
    for duty in range(0, 65535, step):
        led.duty_u16(duty)  # envoye de la variable duty sur le led pwm
        sleep(delay)
    # descente
    for duty in range(65535, 0, -step):
        led.duty_u16(duty)
        sleep(delay)
    led.duty_u16(0)  # LED éteinte à la fin
    
    
'''-----Clignotement sur le lcd------'''
def lcd_blink(text, row=0, col=0, times=0, delay=0.2):
    """
    Fait clignoter un texte sur le LCD.
    text : texte à afficher
    row  : ligne (0 ou 1)
    col  : colonne de départ
    times: nombre de clignotements
    delay: durée de chaque affichage (s)
    """
    for _ in range(times):
        d.clear()   # nettoye l'ecran lcd 
        d.setCursor(col, row) # donne le depart d'affichage sur le lcd 
        d.print(text)     # afficher le texte
        sleep(delay)
        d.setCursor(col, row)
        d.print(" " * len(text))  # effacer le texte
        sleep(delay)

'''-----Defilement du Alarm sur lcd------'''
def lcd_scroll(text, row=0, delay=0.3, repeat=0):
    """
    Fait défiler un texte sur une ligne du LCD.
    text : texte à faire défiler
    row  : ligne sur laquelle le texte défile
    delay: pause entre chaque déplacement (s)
    repeat: nombre de fois que le texte défile complètement
    """
    lcd_width = 16  # largeur de LCD
    # ajoute des espaces à la fin pour un défilement propre
    padded_text = text + " " * lcd_width
    
    for _ in range(repeat):
        for i in range(len(padded_text) - lcd_width + 1):
            d.clear()
            d.setCursor(0, row)
            d.print(padded_text[i:i + lcd_width])
            sleep(delay)

'''-----Main loop-----'''
while True:
    
    '''----Mapping du pot----'''
    val = pot.read_u16()  # lecture brute entre 0 et 65535
    valeur_consigne = 15 + (val * (35 - 15)/65535)  # mappe entre 15 et 35
    print("Set", round(valeur_consigne, 1)) # donne la valeur de set arrondie 
    sleep(0.5)
    
    '''----Lecture du capteur temperature-----'''
    sensor.measure()
    temp=sensor.temperature()
    sleep(1)
    
    '''---Calcul de la difference entre set et ambiant----'''
    diff = temp - valeur_consigne
    print("diff:",round(diff,1))
    
    '''----Affichage sur le LCD------'''
    d.clear()
    d.setCursor(0,0)
    d.print("Temp consigne:"+str(valeur_consigne))
    d.setCursor(0,1)
    d.print("Temp ambiante:"+str(temp))
    
    '''-----Premier etat----'''
    if diff <= 0:
        print("etat 1: pas de problème")
        buzzer.duty_u16(0)#close
        
    #-----Deuxieme etat------
    elif diff < 3 :
        print("etat 2: ca chauffe un peu chef")
        for _ in range(1):
            led_dimmer()
        # Défilement du mot ALARM
        lcd_scroll("!!! ALARM !!!", row=0, delay=0.1, repeat=1)
        
    #-----Troisieme etat------ 
    else:
        print("etat 3: Au feu!!!!!")
        buzzer.freq(1000)	# buzzer sonne 
        buzzer.duty_u16(1000)
        for _ in range(2):
            led_dimmer()
            #clignotement alarm
            lcd_blink("ALARM", row=0, col=0, times=1, delay=0.2)
        buzzer.duty_u16(0)
        d.clear()
        d.setCursor(0,0)
        d.print("ALARM")
    sleep(0.1)  # petite pause pour stabilité
    print("--------------------------------------------")