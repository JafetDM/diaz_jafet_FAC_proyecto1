from machine import Pin, PWM
import utime

# Codigo que agrega el sensor y el buzzer. 

# El buzzer se maneja puramente con la rasberry
# se usa para tener una guia auditiiva de cuando tocar el sensor
# es meramente para ayudar a que sea más facil poner la contraseña 
# en los intervalos del clock

# Los datos se mandan serialmente usando la misma función de antes
# El cambio consiste en que la lista que se lee proviene del sensor
# La lista es meramente un paso para que se lean los datos correctamente
# El sensor tiene mucho ruido y hace muchas lecturas por toque.
# Por lo tanto, se usa la raspberry como debouncer. 
# Se usa una función que toma la primera lectura positiva (si la hay) (read_sensor_deboune)
# De nuevo, esto es para que el sensor lea solo un 1 o se mantenga en 0 si se toca.

# Cabe aclarar que la raspberry no hace ninguna lógica adicional que afecte al sentido
# del circuito. el circuito sigue funcionando con 8 datos que son leídos de forma serial 
# desde el sensor y que son pasados serialmente a paralelo usando el CD4094.
# Este uso de la raspberry se le consultó al profesor en clase y lo aprobó.

# Referencia: 
# https://youtu.be/8It1oVU2BDs?si=wNtgv1tNtvLGFr7i
# Además, se uso ChatGPT para menejo de errores

# Pines Raspberry Pi Pico
data  = Pin(10, Pin.OUT)   # DIN
latch = Pin(11, Pin.OUT)   # CP (clock del shift)
clock = Pin(12, Pin.OUT)   # STROBE (clock del latch)
LED_int = Pin(25, Pin.OUT) # LED integrado
LED_ext = Pin(14, Pin.OUT) # LED externo actividad
sensor = Pin(15, Pin.IN)   # SW-420
buzzer = PWM(Pin(13))      # Buzzer

# Configurar PWM para buzzer
buzzer.freq(1000)
buzzer.duty_u16(0) # apagado

# Debounce simple
def read_sensor_debounced(ms=30):
    if sensor.value():
        utime.sleep_ms(ms)
        if sensor.value():
            return 1
    return 0

# Enviar lista de bits al CD4094
def turnOnLed(status_led):
    latch.value(0)
    for led in status_led:
        clock.value(0)
        data.value(led)
        clock.value(1)
    latch.value(1) #usar para leyendo?

# Hacer sonar buzzer breve
def beep(duration_ms=150):
    buzzer.duty_u16(30000)
    utime.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

# LEDs de actividad
LED_int.value(1)
LED_ext.value(1)

print("Sistema listo. Se capturarán 8 toques, un bit cada segundo.")

while True:
    lista_led = []

    for i in range(8):
        print(f"Preparado para toque {i+1}/8")
        beep(150)            # aviso previo
        utime.sleep(0.5)     # espera breve antes de tomar el toque

        # Espera el toque del sensor
        bit_captured = 0
        timeout = utime.ticks_ms() + 1000  # ventana de 1 segundo
        while utime.ticks_ms() < timeout:
            if read_sensor_debounced(20):
                bit_captured = 1
                break

        lista_led.append(bit_captured)
        print(f"Bit capturado: {bit_captured}")
        utime.sleep_ms(300)  # pequeña pausa antes del siguiente aviso

    # Enviar los 8 bits al CD4094
    turnOnLed(lista_led)
    print("Secuencia enviada al CD4094:", lista_led)

    # Esperar 15 segundos antes de la siguiente secuencia
    print("Esperando 15 segundos antes de la siguiente secuencia...")
    for _ in range(15):
        LED_ext.toggle()  # parpadeo cada segundo
        utime.sleep(1)



