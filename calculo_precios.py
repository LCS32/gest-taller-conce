def calculotunning(precio_nuevo):
    if precio_nuevo >= 200000:
        precio_fulltunning = 136000 
    elif precio_nuevo >50000:
        precio_fulltunning = 30000
    elif precio_nuevo > 20000:
        precio_fulltunning = 12400
    elif precio_nuevo > 9000:
        precio_fulltunning = 9400
    elif precio_nuevo > 0:
        precio_fulltunning = 1100  
    return precio_fulltunning


def calculopintura(precio_nuevo):
    if precio_nuevo >= 200000:
        precio_pintura = 16000
    elif precio_nuevo >50000:
        precio_pintura = 5000
    elif precio_nuevo > 20000:
        precio_pintura = 3000
    elif precio_nuevo > 9000:
        precio_pintura = 2000
    elif precio_nuevo > 0:
        precio_pintura = 300 
    return precio_pintura

def calculocompramos(precio_fulltunning, precio_nuevo):
    precio_compramos = (precio_fulltunning + precio_nuevo)/2
    return precio_compramos

def calculovendemos(precio_nuevo, precio_fulltunning):    
    precio_vendemos = (precio_nuevo + precio_fulltunning)-(precio_nuevo+precio_fulltunning)*0.2
    return precio_vendemos

def calculoestetica (precio_nuevo):
    if precio_nuevo >= 200000:
        precio_estetica = 20000 
    elif precio_nuevo >50000:
        precio_estetica = 5000
    elif precio_nuevo > 20000:
        precio_estetica = 3400
    elif precio_nuevo > 9000:
        precio_estetica = 2400
    elif precio_nuevo > 0:
        precio_estetica = 300  
    return precio_estetica


def calculomotor(precio_nuevo):
    if precio_nuevo >= 200000:
        precio_motor = 100000 
    elif precio_nuevo >50000:
        precio_motor = 20000
    elif precio_nuevo > 20000:
        precio_motor = 6000
    elif precio_nuevo > 9000:
        precio_motor = 5000
    elif precio_nuevo > 0:
        precio_motor = 500  
    return precio_motor

def calculocontrato (precio_nuevo):
    precio_contratos = round (precio_nuevo *1/100+1000,-1)
    return precio_contratos
