from machine import Pin, ADC, PWM # importation des fonctions pin,adc,pwm depuis la librairie machine
from time import sleep #importation de la fonction sleep depuis la librairie time

# --- Hardware setup ---
pot = ADC(0)               # Potentiometer (volume)
buzzer = PWM(Pin(27))      # Buzzer
BP = Pin(18, Pin.IN)       # Button 
state = 0                  # 0: stop, 1: melody1, 2: melody2
led = Pin(16, Pin.OUT)     # LED indicator

# --- Interrupt handler ---
def state_change(pin): #definition de la fonction state_change
    global state 
    state = (state + 1) % 3   # Cycles 0→1→2→0...
    print("State changed to:", state)

BP.irq(trigger=Pin.IRQ_FALLING, handler=state_change) # appelle de la fonction state change pour chaque interruption du bouton 

# --- fonctions ---
def vol(): # fonction pour gerer le volume sonore
    return pot.read_u16()-300 # Pot au min = 275 de valeur en mettant -300 on s'assure que lorsque le pot est au min la valeur vaut bien 0

def play(freq, time): # fonction pour gerer les melodies avec quel frequence de notes et quel timing jouer la note
    if freq == 0: # si frequence a zero alors volume a zero et led eteinte
        buzzer.duty_u16(0)
        led.value(0)
    else: # sinon mettre le buzzer a la fréquence et le volume aux variables indiquer 
        buzzer.freq(freq)
        buzzer.duty_u16(vol())
        led.value(1)
        
    print("Freq:", freq, "Vol:", pot.read_u16())
    sleep(time)
    led.value(0)

# --- Notes ---  # definition des differentes notes avec frequence et duration = variable t
def DO(t): play(1046, t)
def RE(t): play(1175, t)
def MI(t): play(1318, t)
def FA(t): play(1397, t)
def SO(t): play(1568, t)
def LA(t): play(1760, t)
def SI(t): play(1967, t)
def N(t):  play(0, t)


# --- Melodies ---
Melodie1 = [ # Melodie LITTLE STAR
    (DO, 0.25), (N, 0.01), (DO, 0.25), (N, 0.01),
    (SO, 0.25), (N, 0.01), (SO, 0.25), (N, 0.01),
    (LA, 0.25), (N, 0.01), (LA, 0.25), (N, 0.01),
    (SO, 0.5), (N, 0.01), (FA, 0.25), (N, 0.01),
    (FA, 0.25), (N, 0.01), (MI, 0.25), (N, 0.01),
    (MI, 0.25), (N, 0.01), (RE, 0.25), (N, 0.01),
    (RE, 0.25), (N, 0.01), (DO, 0.5), (N, 0.01)
]

Melodie2 = [ # Melodie two_tiger
    (DO, 0.25), (RE, 0.25), (MI, 0.25), (DO, 0.25),
    (N, 0.01), (DO, 0.25), (RE, 0.25), (MI, 0.25),
    (DO, 0.25),(MI, 0.25), (FA, 0.25), (SO, 0.5),
    (MI, 0.25), (FA, 0.25), (SO, 0.5),(N, 0.01),
    (SO, 0.125), (LA, 0.125), (SO, 0.125), (FA, 0.125),
    (MI, 0.25), (DO, 0.25), (SO, 0.125), (LA, 0.125),
    (SO, 0.125),(FA, 0.125), (MI, 0.25), (DO, 0.25),
    (RE, 0.25), (SO, 0.25),(DO, 0.5), (N, 0.01),
    (RE, 0.25), (SO, 0.25), (DO, 0.5)
]

# --- Main loop ---
while True:
    if state == 1:  # si etat = 1 alors Play Melody 1
        for note, duration in Melodie1:
            if state != 1:
                break
            note(duration)
    elif state == 2:  # si etat = 2 alors Play Melody 2
        for note, duration in Melodie2:
            if state != 2:
                break
            note(duration)
    else: # sinon pas de son 
        buzzer.duty_u16(0)
        sleep(0.1)
