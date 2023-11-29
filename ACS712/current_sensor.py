from machine import Pin, ADC
from time import sleep


# Retorna o valor da leitura analogica (0 - 4095) em Volts (0V - 3,3V)
def leitura():
    return pot.read() * 0.805

# Encontra o zero do sensor
def auto_zero():
    print("Calibrando...")
    
    media = 1650 # valor esperado do sensor com corrente nula

    for i in range(1, 10000):
        atual = leitura()
        media = (media + atual) / 2
    
    print("Pronto")
    print("CAL: ", media)
    return media

# Faz a leitura do valor atual da corrente
def valor():

    # Sem divisor de tensão (Sensor out = 2500 mV)
    # valor = pot.read() * 0.805
    # zerado = valor - 2250
    # amps = zerado / 185
    # print("Amps: " + str(round(amps, 1)) + " mV cal: " + str(round(zerado, 1)) + " real: " + str(valor))

    # Com divisor de tensão (Sensor out = 1650 mV)
    valor = leitura()
    zerado = (valor - ZERO_SENSOR)
    amps = zerado / 122
    print("Amps: " + str(round(amps, 1)) + " mV cal: " + str(round(zerado, 1)) + " real: " + str(valor))
    return amps
    

# Inicia comunicação analogica com o sensor usando o pino 34
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB) # amplitude total do sinal 3,3V

# Calibra valores do sensor 
ZERO_SENSOR = auto_zero()

