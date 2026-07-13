from machine import Pin, ADC
import time


def ask(text):
    print(text)
    a = input(">")
    return a


sensor = ADC(Pin(34))
air = 0
water = 0
stan = True
sensor.atten(ADC.ATTN_11DB)

while stan == True:
    b = ask("""
    *PRZYGOTUJ SZKLANKE Z WODĄ*
    
    
            PODŁĄCZ
    ESP32               SENSOR
    GND        <->        GND
    3.3V       <->        VCC
    P34        <->        AOUT
    
    JEŻELI PODŁĄCZYŁEŚ WPISZ YES
    """)
    if b == "YES":
        print("TRZYMAJ CZUJNIK W POWIETRZU NIE DOTYKAJĄC SONDY")
        time.sleep(3)
        air = sensor.read()
        print("ZMIERZONO WARTOŚĆ")
        print("WŁÓŻ CZUJNIK DO SZKLANKI Z WODĄ")
        time.sleep(3)
        water = sensor.read()
        print(f"""
        WARTOŚCI
        
        POWIETRZE - {air}
        WODA - {water}
        
        
        """)
        stan = False
    else:
        print("WŁĄCZ PROGRAM JESZCZE RAZ")
        break
