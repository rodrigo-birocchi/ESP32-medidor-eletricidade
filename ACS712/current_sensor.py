from machine import Pin, ADC
from time import sleep


# Encontra o zero do sensor
def auto_zero():
    print("Calibrando o sensor...")
    menor_valor = 4095

    for i in range(1, 100000):
        valor_atual = pontentiometer.read()
        if valor_atual < menor_valor: menor_valor = valor_atual
    
    print("Pronto")
    print("CAL: ", menor_valor)
    return menor_valor

# Encontra o menor valor no sensor
def menor_valor():
    menor_valor = 4095

    for i in range(1, 10000):
        valor_atual = pontentiometer.read()
        if valor_atual < menor_valor: menor_valor = valor_atual
    
    print("ANC: ", menor_valor)
    return menor_valor

# Faz a leitura do valor atual da corrente
def valor():
    pontentiometer_value = ZERO_SENSOR - menor_valor() # valor no pino analogico calibrado com zero do sensor
    volts_value = pontentiometer_value * 0.805 # amplitude total / resolucao da maquina = valor em volts
    final_value = round(volts_value / 185, 1) # de acordo com a datasheet do ACS712-05B
    print("CALC: ", final_value)
    return final_value
    

# Inicia comunicação analogica com o sensor usando o pino 32
pontentiometer = ADC(Pin(32))
pontentiometer.atten(ADC.ATTN_11DB) # amplitude total do sinal 3,3V

# Calibra valores do sensor 
ZERO_SENSOR = auto_zero()

