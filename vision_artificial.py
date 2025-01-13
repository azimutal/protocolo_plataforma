from random import random
import time
from constantes import *
from mensajes_control import * 
from colorama import Fore
from conexion_platforma import ComunicacionControlPlataforma
import threading

COMANDO_ENVIAR_MENSAJE_INDICANDO_QUE_HAY_VISIBILIDAD_BAJA = 1
COMANDO_SALIR = 2

mensajes_por_segundo = 1
enviar_streaming = False
finalizar = False

def callback_comando(comando, valor):
    global enviar_streaming
    global mensajes_por_segundo

    if comando == MENSAJE_ESTABLECER_MENSAJES_POR_SEGUNDO:
        mensajes_por_segundo = int(valor)
        print(Fore.GREEN + 'Velocidad de mensajes por segundo establecida a: {}'.format(mensajes_por_segundo))
    elif comando == MENSAJE_COMENZAR_STREAMING:
        enviar_streaming = True
        print(Fore.GREEN + 'El cliente ha solicitado comenzar el streaming')
    elif comando == MENSAJE_FINALIZAR_STREAMING:
        enviar_streaming = False
        print(Fore.GREEN + 'El cliente ha solicitado finalizar el streaming')
    else:
        print(Fore.RED + 'Recibido el comando desconocido: Comando={}, Valor={}'.format(comando, valor))

# La clase ComunicacionControlPlataforma crea un servidor si se pasa el parámetro callbackMensajeRecibido.
# Al crear un servidor, en la dirección ponemos '' para indicar que escuche en todas las interfaces de red.
servidor_mensaje = ComunicacionControlPlataforma(
    ('', PUERTO_MENSAJES_VISION_ARTIFICIAL),
    errorCallback=lambda error: print(Fore.RED + '\nSe ha detectado el siguiente error: {}'.format(error)),
    conectadoCallback=lambda conectado: print(Fore.GREEN + 'Conectado={}'.format(conectado)),
    tamanoPaqueteRecepcion = TAMANO_MENSAJE_CONTROL,
    callbackMensajeRecibido=callback_bytes_a_comando(callback_comando))

# La clase ComunicacionControlPlataforma crea un cliente si no se pasa el parámetro callbackMensajeRecibido.
# Al crear un cliente, en la dirección ponemos la dirección del servidor al que nos queremos conectar.
cliente = ComunicacionControlPlataforma(
    (DIRECCION_VISION_ARTIFICIAL, PUERTO_MENSAJES_PLATAFORMA),
    errorCallback=lambda error: print(Fore.RED + '\nSe ha detectado el siguiente error: {}'.format(error)),
    conectadoCallback=lambda conectado: print(Fore.GREEN + 'Conectado={}'.format(conectado)),
    tamanoPaqueteRecepcion = TAMANO_MENSAJE_CONTROL)

cliente_streaming = ComunicacionControlPlataforma(
    (DIRECCION_VISION_ARTIFICIAL, PUERTO_STREAMING),
    errorCallback=lambda error: print(Fore.RED + '\nSe ha detectado el siguiente error: {}'.format(error)),
    conectadoCallback=lambda conectado: print(Fore.GREEN + 'Conectado={}'.format(conectado)),
    tamanoPaqueteRecepcion = TAMANO_MENSAJE_STREAMING)

def menu_opciones():
    print(Fore.WHITE + f"{COMANDO_ENVIAR_MENSAJE_INDICANDO_QUE_HAY_VISIBILIDAD_BAJA}. Comunicar baja visibilidad.")
    print(Fore.WHITE + f"{COMANDO_SALIR}. Salir.")
    opcion = int(input("Seleccione una opción: "))
    return opcion

def bucle_envia_mensajes_streaming():
    while not finalizar:
        if enviar_streaming:
            cliente_streaming.EnviaDatos(crea_mensaje_streaming(random(), random(), random()))
            time.sleep(1 / mensajes_por_segundo)
        else:
            time.sleep(1)
            
threading.Thread(target=bucle_envia_mensajes_streaming).start()

while True:
    try:
        opcion = menu_opciones()
        if opcion == COMANDO_SALIR:
            finalizar = True
            break
        elif opcion == COMANDO_ENVIAR_MENSAJE_INDICANDO_QUE_HAY_VISIBILIDAD_BAJA:
            cliente.EnviaDatos(crea_mensaje_visibilidad_baja())
        else:
            print("Opción no válida")
    except ValueError:
        print("error")
