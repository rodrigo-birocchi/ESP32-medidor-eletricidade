from ACS712 import current_sensor as cs

def potencia_atual():
    return cs.valor()
