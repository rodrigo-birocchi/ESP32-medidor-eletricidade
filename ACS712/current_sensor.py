from machine import Pin, ADC
from time import sleep


# Encontra o zero do sensor
def auto_zero():
    print("Fazendo ao auto zero do sensor...")
    menor_valor = 4095

    for i in range(1, 10000):
        valor_atual = pontentiometer.read()
        if valor_atual < menor_valor: menor_valor = valor_atual
        sleep(1/1000000) # espere 1 microsegundo

    return menor_valor

# Encontra o menor valor no sensor
def menor_valor():
    menor_valor = 4095

    for i in range(1, 1600):
        valor_atual = pontentiometer.read()
        if valor_atual < menor_valor: menor_valor = valor_atual
        sleep(1/100000) # espere 10 microsegundos

    return menor_valor

# Faz a leitura do valor atual da corrente
def valor():
    pontentiometer_value = ZERO_SENSOR - menor_valor() # valor no pino analogico calibrado com zero do sensor
    volts_value = pontentiometer_value * 0.805 # amplitude total / resolucao da maquina = valor em volts
    final_value = volts_value / 185 # de acordo com a datasheet do ACS712-05B
    return final_value

# Mostra resultados no console com formatação
def print_result(res):
    print("Corrente de pico:")
    print(str(res) + "A")
    print("-----------------")
    print(str(res * 1000) + "mA")
    

# Inicia comunicação analogica com o sensor usando o pino 32
pontentiometer = ADC(Pin(32))
pontentiometer.atten(ADC.ATTN_11DB) # amplitude total do sinal 3,3V

# Calibra valores do sensor 
ZERO_SENSOR = auto_zero()
