#======= LABO_5 ===============
import network
import time
import ntptime
from machine import Pin, Timer
from servo import SERVO
from utime import sleep ,ticks_ms, ticks_diff

# === CONFIGURATION WI-FI ===
SSID = '***********'
PASSWORD = '***********'

# === CONFIGURATION SERVO ===
servo = SERVO(Pin(20))  # Broche de signal du servo

# === BOUTON ==========
button = Pin(18, Pin.IN) # Broche de signal boutton

#===== VARIABLES GLOBALES ===============
timezone = 1  # Démarre en UTC+1 (France)
last_press = 0  # anti-rebond
mode_24h = False # Variables du mode 24H ou 12H 
last_click = 0
click_timer = Timer()
debounce_ms = 150 # Variables pour anti-rebond
double_ms = 500 # Variable pour le double click
multi_click_guard = 700  # Délai mini entre deux clics simples successifs

''' ======= FONCTIONS ========== '''
def connect_wifi(): 
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connexion au Wi-Fi...")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\n✅ Connecté au Wi-Fi ! IP :", wlan.ifconfig()[0])

def get_time_internet(offset=0):
    print("⏳ Synchronisation NTP...")
    try:
        ntptime.settime()
        print("✅ Heure récupérée depuis Internet !")
        # Décalage selon fuseau horaire
        t = time.localtime(time.time() + offset * 3600)
        return t[3], t[4]  # heure, minute
    except Exception as e:
        print("❌ Erreur lors de la récupération de l'heure :", e)
        return None, None

def servo_angle(angle):
    # Convertit un angle (0–150°) en signal PWM
    duty = int(1638 + (angle / 150) * (7372 - 1638))
    servo.turn(duty)

def heure_to_angle(heure, minute=0):
    """Convertit l'heure en angle selon le mode (12h ou 24h)"""
    if mode_24h:
        # 24h → 0–150° (6.25° par heure)
        angle = (heure + minute / 60) * 6.25
    else:
        # 12h → 0–150° (12.5° par heure)
        heure_12 = heure % 12
        angle = (heure_12 + minute / 60) * 12.5
    return angle

''' --- Gestionnaire d'interruption Bouton --- '''

def single_click_action(t):
    """Exécuté si aucun 2e clic dans la fenêtre double_ms"""
    global last_click, timezone
    if last_click != 0:
        timezone += 1
        if timezone > 12:
            timezone = -12
        print(f"🌍 Fuseau horaire → UTC{timezone:+d}")
    last_click = 0
    
    
def state_change(pin):
    """Un clic = change fuseau, double clic rapide = bascule 24h/12h"""
    global last_press, mode_24h, click_timer, last_click
    
    current = ticks_ms()
    delay = ticks_diff(current,last_press)

    # Anti-rebond
    if delay < debounce_ms:
        return
    last_press = current
    

     # Double clic détecté ?
    if last_click != 0 and ticks_diff(current,last_click) < double_ms :
        mode_24h = not mode_24h
        print(f"🕓 Mode {'24H' if mode_24h else '12H'} activé")
        try:
            click_timer.deinit()
        except:
            pass
        last_click = 0
        return
    
    # --- Cas du clic simple ---
    # Empêche que des clics trop rapprochés soient mal interprétés
    if last_click != 0 and ticks_diff(current, last_click) < multi_click_guard:
        # Ignorer les clics trop rapprochés pour éviter confusions
        return
    
    # Premier clic, démarrer timer pour simple clic
    last_click = current 
    try:
        click_timer.deinit()
    except:
        pass
    click_timer.init(mode=Timer.ONE_SHOT, period=double_ms, callback=single_click_action)
    
    
# Attache l’interruption sur front descendant
button.irq(trigger=Pin.IRQ_FALLING, handler=state_change)

# === PROGRAMME PRINCIPAL ===
print("=== HORLOGE SERVO AUTOMATIQUE (Wi-Fi + NTP) ===")

# Mode Wi-Fi
connect_wifi()
print("Appuie sur le bouton pour changer de fuseau horaire (UTC±).")
print("Double clic pour basculer entre mode 12H et 24H.")

while True:
    heure, minute = get_time_internet(timezone)
    if heure is not None:
        angle = heure_to_angle(heure, minute)
        print("🕒 Fuseau UTC{:+d} → {:02d}:{:02d} → Servo : {:.1f}°".format(timezone, heure, minute, angle))
        print(f"🕒 {'24H' if mode_24h else '12H'} | UTC{timezone:+d} → {heure:02d}:{minute:02d} → {angle:.1f}°")
        servo.turn(angle)
    else:
        print("⚠️ Impossible de récupérer l'heure.")
    sleep(2)  # Actualisation toutes les 10 secondes
    print("================================================================")
