#Programme exercice 1 Bonus

import machine
import utime


Led = machine.Pin(16,machine.Pin.OUT)
BP=machine.Pin(18,machine.Pin.IN)
state=0

def state_change(Pin):#definition de la fonction interruption 
    global state
    state=state+1
    print("state change")
    
BP.irq(trigger=machine.Pin.IRQ_FALLING,handler=state_change)
#utilisation de la fonction interruption

while True:
#C'est egal au void loop dans arduino c'est ca qui fait la boucle"
        
#Gestion de la led independament du reste"
    if state == 0: #Etat = 0 => led eteinte"
        Led.value(0)
        utime.sleep(2)
        print(f"state:{state}")#information de l'etat affichage de la valeur
        
        
    elif state ==2 or state==3: #"Etat = 1 => led clignote 0,5Hz"
        Led.value(1)
        utime.sleep(1)
        Led.value(0)
        utime.sleep(1)
        print(f"state:{state}")
        
        
    elif state == 4 or state==5: #"Etat = 2 => led clignote differement 
        Led.value(1)
        utime.sleep(0.25)
        Led.value(0)
        utime.sleep(0.25)
        Led.value(1)
        utime.sleep(0.50)
        Led.value(0)
        utime.sleep(0.50)
        Led.value(1)
        utime.sleep(1)
        Led.value(0)
        utime.sleep(1)
        print(f"state:{state}")
        
        
    elif state == 6:#remise a zero de l'etat la led s'eteint
        state=0
        print(f"state:{state}")
