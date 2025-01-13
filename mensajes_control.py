import struct

MENSAJE_ESTABLECER_MENSAJES_POR_SEGUNDO = 1
MENSAJE_COMENZAR_STREAMING = 2
MENSAJE_FINALIZAR_STREAMING = 3
MENSAJE_VISIBILIDAD_BAJA = 5

# Los mensajes de control tienen el formato [comando, valor]. El comando es un entero de 2 bytes y el valor un float de 8.
TAMANO_MENSAJE_CONTROL = 10

# Los mensajes de streaming tienen el formato [delay, azimut, elevacion]. Todos los valores son floats de 8 bytes.
TAMANO_MENSAJE_STREAMING = 24

# La clase conexion_platforma.ComunicacionControlPlataforma espera recibir un callback que reciba un parámetro bytes con el mensaje,
# pero a nosotros nos interesa pasarle una función que reciba dos parámetros, comando y valor. Por eso, creamos una función que reciba
# el parámetro bytes y lo desempaquete en comando y valor.
def callback_bytes_a_comando(callback):
    def callback_control(bytes):
        comando, valor = struct.unpack('if', bytes)
        callback(comando, valor)
    return callback_control
    
def crea_mensaje_establecer_mensajes_por_segundo(velocidad):
    return struct.pack('if', MENSAJE_ESTABLECER_MENSAJES_POR_SEGUNDO, velocidad)

def crea_mensaje_comenzar_streaming():
    return struct.pack('if', MENSAJE_COMENZAR_STREAMING, 0)

def crea_mensaje_finalizar_streaming():
    return struct.pack('if', MENSAJE_FINALIZAR_STREAMING, 0)

def crea_mensaje_visibilidad_baja():
    return struct.pack('if', MENSAJE_VISIBILIDAD_BAJA, 0)

def crea_mensaje_streaming(delay, azimut, elevacion):
    return struct.pack('ddd', delay, azimut, elevacion)


