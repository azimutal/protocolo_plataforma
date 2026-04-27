# PROTOCOLO_PLATAFORMA

Este repositorio implementa dos programas de consola: 

* [plataforma.py](plataforma.py). Este programa simula el software de plataforma con el que interactúa el usuario.
* [vision_artificial.py](vision_artificial.py). Este programa simula el servicio de visión artificial.

## Comunicación entre los dos procesos

La comunicación entre los dos programas se realiza mediante la clase `conexion_plataforma.ComunicacionControlPlataforma`. Esta clase permite crear servidores y clientes _TCP_ y _UDP_. 

El protocolo _UDP_ es mucho más rápido que el _TCP_, pero no garantiza la entrega de los paquetes ni el orden de los mismos, pero como trabajamos con una conexión local no hay posibilidad de que pase ninguno de estos dos problemas así que trabajaremos con _UDP_.

En el protocolo _TCP_ se establece un canal de comunicación entre dos equipos y se puede utilizar este canal para enviar y recibir datos. Como en _UDP_ no tenemos este canal, tendremos que crear tantos canales unidireccionales distintos como sea necesario.

En el módulo [constantes.py](constantes.py) se definen las constantes:

- `PUERTO_STREAMING` que es el puerto por el que esta aplicación recibe los datos de visión artificial.
- `PUERTO_MENSAJES_PLATAFORMA` que es el puerto por el que esta aplicación recibe los mensajes enviados por la visión artificial.
- `PUERTO_MENSAJES_VISION_ARTIFICIAL` que es el puerto por el que esta aplicación enviará mensajes al programa de visión artificial.

## Mensajes de control

Los mensajes de control que se envían ambos programas son un stream de 10 bytes con la siguiente estructura:

- 2 bytes para el comando (entero).
- 8 bytes para el valor opcional (float). Si el mensaje no requiere un valor, se envía aquí un 0, pero da igual lo que se envíe, pues no se va a utilizar este valor.

Podemos crear los mensajes que nos interesen. Este ejemplo implementa los siguientes mensajes (definidos en el módulo [mensajes_control.py](mensajes_control.py)):

- `MENSAJE_ESTABLECER_MENSAJES_POR_SEGUNDO`.
- `MENSAJE_COMENZAR_STREAMING`.
- `MENSAJE_FINALIZAR_STREAMING`.
- `MENSAJE_VISIBILIDAD_BAJA`.

Este módulo implementa funciones para crear estos mensajes (`crea_mensaje_establecer_mensajes_por_segundo`, `crea_mensaje_comenzar_streaming`, `crea_mensaje_finalizar_streaming` y `crea_mensaje_visibilidad_baja`).

## Mensajes de streaming

El programa de visión artificial envía un streaming de datos al programa de plataforma. En este ejemplo nos hemos inventado un mensaje formado por tres valores de tipo float que son:

- 8 bytes para el delay.
- 8 bytes para el azimut.
- 8 bytes para la elevación.

## Programa plataforma.py

Al ejecutar este programa se crea:

- Un servidor que recibirá mensajes del servicio de visión artificial.
- Un servidor que recibirá el streaming del servicio de visión artificial.
- Un cliente que enviará mensajes al servicio de visión artificial.

Luego muestra el siguiente menú de opciones al usuario:

1. Enviar configuración de velocidad al programa de visión artificial. 
2. Comenzar streaming visión artificial. 
3. Finalizar streaming visión artificial.
4. Salir. 

La primera opción solicita al usuario un valor de velocidad (que no sirve para nada, es por un ejemplo enviar un parámetro a visión artificial). Se crea el mensaje `MENSAJE_ESTABLECER_MENSAJES_POR_SEGUNDO` y se envía por el puerto `PUERTO_MENSAJES_VISION_ARTIFICIAL`.
La segunda opción comienza el streaming de visión artificial. Se crea el mensaje `MENSAJE_COMENZAR_STREAMING` y se envía por el puerto `PUERTO_MENSAJES_VISION_ARTIFICIAL`.
La tercera finaliza el streaming. Se crea el mensaje `MENSAJE_FINALIZAR_STREAMING` y se envía por el puerto `PUERTO_MENSAJES_VISION_ARTIFICIAL`.
La cuarta opción finaliza el programa.

## Programa vision_artificial.py

Al ejecutar este programa se crea:

- Un servidor que recibirá mensajes del programa plataforma.
- Un cliente que enviará el mensaje `MENSAJE_VISIBILIDAD_BAJA` al programa de plataforma.
- Un cliente que enviará el streaming cuando este se habilite.

Luego muestra el siguiente menú de opciones al usuario:

1. Comunicar baja visibilidad. 
2. Salir. 

Si el usuario selecciona la primera opción, se enviará un mensaje al programa de plataforma para indicar que han cambiado las condiciones de visibilidad.
Si el usuario selecciona la segunda opción se finalizará el programa.

## Programa .NET para la lectura y comprobación de herztios

Se ha añadido un pequeño programa de consola en el lenguaje C# que es idéntico al que se está utilizando en la aplicación final.

Para compilar y ejecutar este programa en Linux, ejecutaremos la siguiente secuencia de comandos:

```bash
sudo apt install dotnet-sdk-10.0
dotnet build
dotnet run
```