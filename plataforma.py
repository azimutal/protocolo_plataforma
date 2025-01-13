from constantes import *
from mensajes_control import * 
from colorama import Fore
from conexion_platforma import ComunicacionControlPlataforma
import struct

COMANDO_ESTABLECER_VELOCIDAD = 1
COMANDO_COMENZAR_STREAMING = 2
COMANDO_FINALIZAR_STREAMING = 3
COMANDO_SALIR = 4

def callback_comando(comando, valor):
    if comando == MENSAJE_VISIBILIDAD_BAJA:
        print(Fore.YELLOW + 'Visibilidad baja detectada')
    else:
        print(Fore.RED + 'Recibido el comando desconocido: Comando={}, Valor={}'.format(comando, valor))

def callback_vision_artificial(bytes):
    delay, var_azimut, var_elevacion = struct.unpack('ddd', bytes)
    print(Fore.MAGENTA + 'Recibidos: delay={}, azimut={}, elevación={}'.format(delay,var_azimut, var_elevacion))

# La clase ComunicacionControlPlataforma crea un servidor si se pasa el parámetro callbackMensajeRecibido.
# Al crear un servidor, en la dirección ponemos '' para indicar que escuche en todas las interfaces de red.
servidor_mensaje = ComunicacionControlPlataforma(
    ('', PUERTO_MENSAJES_PLATAFORMA),
    errorCallback=lambda error: print(Fore.RED + '\nSe ha detectado el siguiente error: {}'.format(error)),
    conectadoCallback=lambda conectado: print(Fore.GREEN + 'Conectado={}'.format(conectado)),
    tamanoPaqueteRecepcion = TAMANO_MENSAJE_CONTROL,
    callbackMensajeRecibido=callback_bytes_a_comando(callback_comando))

servidor_streaming = ComunicacionControlPlataforma(
    ('', PUERTO_STREAMING),
    errorCallback=lambda error: print(Fore.RED + '\nSe ha detectado el siguiente error: {}'.format(error)),
    conectadoCallback=lambda conectado: print(Fore.GREEN + 'Conectado={}'.format(conectado)),
    tamanoPaqueteRecepcion = TAMANO_MENSAJE_STREAMING,
    callbackMensajeRecibido=callback_vision_artificial)

# La clase ComunicacionControlPlataforma crea un cliente si no se pasa el parámetro callbackMensajeRecibido.
# Al crear un cliente, en la dirección ponemos la dirección del servidor al que nos queremos conectar.
cliente = ComunicacionControlPlataforma(
    (DIRECCION_VISION_ARTIFICIAL, PUERTO_MENSAJES_VISION_ARTIFICIAL),
    errorCallback=lambda error: print(Fore.RED + '\nSe ha detectado el siguiente error: {}'.format(error)),
    conectadoCallback=lambda conectado: print(Fore.GREEN + 'Conectado={}'.format(conectado)),
    tamanoPaqueteRecepcion = TAMANO_MENSAJE_CONTROL)

def menu_opciones():
    print(Fore.WHITE + f"{COMANDO_ESTABLECER_VELOCIDAD}. Establecer la velocidad del streaming.")
    print(Fore.WHITE + f"{COMANDO_COMENZAR_STREAMING}. Comenzar streaming visión artificial.")
    print(Fore.WHITE + f"{COMANDO_FINALIZAR_STREAMING}. Finalizar streaming visión artificial.")  
    print(Fore.WHITE + f"{COMANDO_SALIR}. Salir.")
    opcion = int(input("Seleccione una opción: "))
    return opcion

while True:
    try:
        opcion = menu_opciones()
        if opcion == COMANDO_SALIR:
            break
        elif opcion == COMANDO_ESTABLECER_VELOCIDAD:
            velocidad = float(input("Velocidad de streaming: "))
            cliente.EnviaDatos(crea_mensaje_establecer_mensajes_por_segundo(velocidad))
        elif opcion == COMANDO_COMENZAR_STREAMING:
            cliente.EnviaDatos(crea_mensaje_comenzar_streaming())
        elif opcion == COMANDO_FINALIZAR_STREAMING:
            cliente.EnviaDatos(crea_mensaje_finalizar_streaming())
        else:
            print("Opción no válida")
    except ValueError:
        print("error")
