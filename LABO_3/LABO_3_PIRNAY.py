'''Programme de l'exercice 3'''

'''---Librairie setup-----'''
from LCD1602 import LCD1602 		#importation de la fonction LCD1602 depuis la librairie LCD1602. 
from dht import DHT11  				# importation de la fonction DHT11 depuis la librairie dht.
from machine import I2C,Pin,ADC,PWM # importation des fonctions pin,adc,pwm,i2c depuis la librairie machine.
from utime import sleep 			#importation de la fonction sleep depuis la librairie time.


'''---Hardware setup----'''
pot = ADC(0)				#potentiometre raccorder sur ADC0 soit A0 sur la carte.
led = Pin(20,Pin.OUT)		# led raccorder sur Pin 20 soit D20 sur la carte.
sensor = DHT11(Pin(18)) 	#Initialise le capteur DHT11 connecté sur D18 de la carte.
buzzer = PWM(Pin(16))   	#Crée un signal PWM (modulation de largeur d’impulsion) sur la broche 16.

i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000) # Initialise le bus I²C numéro 1.
                                                 # scl (clock) sur la broche GPIO7 et sda (data) sur GPIO6. Vitesse du bus : 400 kHz.
d = LCD1602(i2c, 2, 16) 						 #Crée un objet d pour piloter un écran LCD 16 colonnes × 2 lignes via I²C.
d.display() 									 # active l’affichage (allume l’écran).



'''-----Main loop-----'''
while True:
    
    '''----Mapping du pot----'''
    val = pot.read_u16()  # lecture brute entre 0 et 65535
    valeur_consigne = 15 + (val * (35 - 15)/65535)  # mappe entre 15 et 35
    print("Set", round(valeur_consigne, 1))
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
        led.value(1)   # allume la LED
        sleep(1)       # attend 1 seconde
        led.value(0)   # éteint la LED
        sleep(1) 	   # attend 1 seconde
        
    #-----Troisieme etat------
    else:
        print("etat 3: Au feu!!!!!")
        buzzer.freq(1000)	# buzzer sonne 
        buzzer.duty_u16(1000)
        led.value(1)  		# allume la LED
        sleep(0.25)       	# attend 1 seconde
        led.value(0)   		# éteint la LED
        sleep(0.25)
        d.clear()
        d.setCursor(0,0)
        d.print("ALARM")
        
    print("--------------------------------------------")