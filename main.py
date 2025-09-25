from machine import Pin
import utime

# Codigo para probar el CD4094, el cual es similar al HC595
# 
# Referencia: https://youtu.be/8It1oVU2BDs?si=wNtgv1tNtvLGFr7i

# Pines Raspberry Pi Pico
data  = Pin(10, Pin.OUT)   # DIN
latch = Pin(11, Pin.OUT)   # CP (shift clock)
clock = Pin(12, Pin.OUT)   # STROBE (latch clock)
LED_int = Pin(25, Pin.OUT) # LED integrado
LED_ext = Pin(14, Pin.OUT) # LED externo para indicar actividad

# Función para encender LEDs 
def turnOnLed(status_led):
    latch.value(0)
    for led in status_led:
        clock.value(0)
        data.value(led)
        clock.value(1)
    latch.value(1)

# Lista de ejemplo 
lista_led = [1, 1, 0, 0, 0, 1, 1, 0]

# Encender LED integrado y externo para indicar que el programa está activo
LED_int.value(1)
LED_ext.value(1)

# Mandar datos 
turnOnLed(lista_led)

# parpadeo del LED externo cada segundo para ver actividad
while True:
    LED_ext.toggle()  # alterna encendido/apagado
    utime.sleep(1)



