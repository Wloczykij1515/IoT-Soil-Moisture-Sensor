from machine import Pin, ADC
import time


class SoilMoistureSensor:
    def __init__(self, pin_adc, pin_vcc, air_val, water_val):
        self.air = air_val
        self.water = water_val

        self.sensor = ADC(Pin(pin_adc))
        self.sensor.atten(ADC.ATTN_11DB)

        self.vcc = Pin(pin_vcc, Pin.OUT)
        self.vcc.value(0)

    def read_raw(self):
        self.vcc.value(1)
        time.sleep(0.2)

        wartosc = self.sensor.read()

        self.vcc.value(0)
        return wartosc

    def percent(self):
        raw = self.read_raw()


        procent = ((raw - self.air) / (self.water - self.air)) * 100
        procent = round(procent)


        if procent < 0:
            procent = 0
        elif procent > 100:
            procent = 100

        return procent