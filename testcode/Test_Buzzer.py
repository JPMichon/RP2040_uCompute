from machine import Pin, PWM
import utime 
import buzzer_music


Buzzer_system=11 # définition du port pour le buzzer (GP9)


def SoundTest():
    Buzzer = PWM(Pin(Buzzer_system)) # initialisation de la pin en PWM
    Buzzer.duty_u16(2000)
    Buzzer.freq(494)
    utime.sleep(.2)
    Buzzer.freq(440)
    utime.sleep(.2)
    Buzzer.freq(392)
    utime.sleep(.2)
    Buzzer.freq(330)
    utime.sleep(.2)
    Buzzer.freq(440)
    utime.sleep(.2)
    Buzzer.duty_u16(0)
    
while True:
    SoundTest()
    utime.sleep(1)