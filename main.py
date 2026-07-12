import time
from machine import Pin, deepsleep
from umqtt.simple import MQTTClient
import network
from config import WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USER, MQTT_PASS, air, water, TOPIC_PUB, zasilanie, sygnal
from sensors import SoilMoistureSensor


#		łączenie z wifi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Łączenie z {WIFI_SSID}")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        #		limit czasu, w momencie gdy router padnie esp nie rozladowuje baterii
        timeout = 0
        while not wlan.isconnected() and timeout < 20:
            time.sleep(0.5)
            timeout += 1

    if wlan.isconnected():
        print(f"Połączono z {WIFI_SSID}! IP:", wlan.ifconfig()[0])
        return True
    else:
        print(f"Nie udało się połączyć z {WIFI_SSID}")
        return False


#			GŁÓWNA LOGIKA

#		łączenie z wifi
if connect_wifi():
    try:
        #		łączenie z MQTT
        print(f"Łączenie z brokerem MQTT {MQTT_BROKER}")
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASS)
        client.connect()

        #		odczytanie danych i ich wysył
        procenty = SoilMoistureSensor(pin_adc=sygnal, pin_vcc=zasilanie, air_val=air, water_val=water)
        wilgotnosc = procenty.percent()
        msg = f"{wilgotnosc}%"
        client.publish(TOPIC_PUB, msg.encode(), retain=True)
        print(f"Wysłano: {msg}")

        #		rozłączenie z MQTT
        client.disconnect()

    except Exception as e:
        print("Błąd podczas komunikacji:", e)
else:
    print("Pomijanie wysyłania ze względu na brak Wi-Fi.")

#			deepsleep
time.sleep(0.5)
DEEP_SLEEP_TIME_MS = 10 * 60 * 1000

print(f"Wchodzę w stan Deep Sleep na {DEEP_SLEEP_TIME_MS / 1000 / 60} minut")
deepsleep(DEEP_SLEEP_TIME_MS)
