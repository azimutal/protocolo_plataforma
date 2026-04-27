import socket
import threading
import time

'''
Este módulo implementa las comunicaciones con el servidor Sair.
'''
class ComunicacionControlPlataforma:
    '''
    Implementa un objeto que establece comunicación con el servidor Sair de manera indefinida. 
    Si se detecta que se ha perdido la conexión, reestablece la conexión indefinidamente.
    Una vez establecida la conexión, admite que se le envíen mensajes.
    Además dispone de callbacks para comunicar al cliente eventos de conexión, mensajes de error, etc. 
    '''
    def __init__(self, direccion, tamanoPaqueteRecepcion=0, segundosAEsperarSiConexionFallida=2, udp=True, conectadoCallback=None, errorCallback=None, callbackMensajeRecibido=None):
        '''
        Inicializa el objeto.
        Argumentos:
            direccion: Tupla (host, puerto) con la dirección en la que conectar.
            segundosAEsperarSiConexionFallida: Segundos a esperar entre intentos de conexión.
            udp: Indica si utilizar el procolo UDP o TCP
            conectadoCallback: Función callback (recibe como parámetro un booleano) para notificar 
                               que se ha establecido o no la conexión. Si se especifica, cuando se consigue conectar
                               se le llamará pasando como parámetro un valor True. Si se pierde la conexión, se llamará
                               pasando un valor False para que el cliente sepa que se ha perdido la conexión.
            errorCallback: Función callback (recibe como parámetro el mensaje de error) para notificar cuando se
                           produce un error.
            callbackMensajeRecibido: Callback al que se llamará cuando se recibe un mensaje.             
        '''
        self._direccion = direccion
        self._tamanoPaqueteRecepcion = tamanoPaqueteRecepcion
        self._segundosAEsperarSiConexionFallida = segundosAEsperarSiConexionFallida
        self._conectadoCallback = conectadoCallback
        self._errorCallback = errorCallback
        self._callbackMensajeRecibido = callbackMensajeRecibido
        self._sock = None
        self._sockRecibir = None
        self._finalizar = False
        self.Conectado = False
        self.MensajesNoEnviados = 0
        self.MensajesEnviados = 0
        self.ConexionesFallidas = 0
        self.ConexionesEstablecidas = 0
        self.ConexionesPerdidas = 0
        self.MensajesRecibidos = 0
        self._udp = udp

        self._reconecta()

    def Close(self):
        '''
        Finaliza los hilos de ejecución y cierra el socket en caso de que estuviera conectado
        '''
        self._finalizar = True
        if self._sock != None:
            self._sock.close()
            self._sock = None

    def EnviaDatos(self, bytes):
        '''
        Envía datos a la plataforma.
        En caso de detectarse un error de conexión, comunicará la desconexión llamando al callback,
        incrementará el número de desconexiones y establecerá la conexión
        '''
        if self._udp:
            self._sock.sendto(bytes, self._direccion)
            self.MensajesNoEnviados += 1
            return

        if self._sock == None:
            self.MensajesNoEnviados += 1
            return
        
        try:
            self._sock.sendall(bytes)
            self.MensajesEnviados += 1
        except ConnectionResetError as error:
            self.ConexionesPerdidas += 1
            if self._errorCallback != None:
                self._errorCallback(error)
            self._reconecta()
      
    def _reconecta(self):
        self._sock = None
        self.Conectado = False
        if self._conectadoCallback != None:
            self._conectadoCallback(False)
        if not self._finalizar:
            threading.Thread(target=self._conectaAsync).start()

    def _conectaAsync(self):

        while(self._sock is None and self._finalizar == False):
            sock = None
            
            if self._udp:
                if self._callbackMensajeRecibido is None:
                    # Protocolo UDP y no se ha especificado callback de recepción, lo que significa que el usuario de este objeto
                    # sólo quiere enviar datos, no recibir
                    sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(None)

                try:
                    sock.connect(self._direccion)
                except ConnectionRefusedError as error:
                    self.ConexionesFallidas += 1
                    if self._errorCallback != None:
                        self._errorCallback(error)
                    time.sleep(self._segundosAEsperarSiConexionFallida)
                    continue

            self._sock = sock

            if self._callbackMensajeRecibido is not None:
                threading.Thread(target=self._recibeAsync).start()

            self.ConexionesEstablecidas += 1
            self.Conectado = True
            if self._conectadoCallback != None:
                self._conectadoCallback(True)
            return

    def _recibeAsync(self):
        if self._udp:            
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.bind(self._direccion)
            self._sock.settimeout(10)

            while(self._sock is not None and self._finalizar == False):
                try:
                    dato_recibido = self._sock.recvfrom(24)[0]
                    self._callbackMensajeRecibido(dato_recibido)
                except Exception as e:
                    if self._finalizar:
                        self._sock.close()
                        break
        else:
            while(self._sock is not None and self._finalizar == False):
                try:
                    bytes = self._sock.recv(self._tamanoPaqueteRecepcion)
                    self._callbackMensajeRecibido(bytes)
                except ConnectionResetError as error:
                    self.ConexionesPerdidas += 1
                
                    if self._errorCallback != None:
                        self._errorCallback(error)
                        self._reconecta()


if __name__ == "__main__":
    print('Este módulo no es ejecutable')