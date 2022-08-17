Bienvenidx al programa de estabilización de diodos láser del DLC pro.

-----------------------------------------------------------------------------------------------------------------------

Para usar el programa debe tener instaladas las librerías de PySimpleGUI y de toptica.

$ pip install --upgrade toptica_lasersdk
$ pip install PySimpleGUI

EL programa se incia corriendo en python (ya sea en spyder o en la terminal)
el archivo "DLC_Stabilization.py" ubicandose en la carpeda donde todos los archivos guardados.

Todos los archivos son "PID_CLASS.py", "_CLIENT_SERVER_DLC_CLASS_.py" y "saveData.txt".

En el "saveData.txt" se encuentran toda la información de la interfaz, los parámetros del PID, y la última tanda de
mediciones de frecuencia, corriente, voltaje.

-----------------------------------------------------------------------------------------------------------------------

Por último, debe abrir el server en la computadora en donde esté conectada el Wavelenght Meter.

Para ello corra el archivo "_server_PID_.py". En el mismo debe indicar el puerto a través del cual se hace la conexión.
En la misma carpeta debe figurar el archivo "wlmData.dll", que es la librería que contiene las funciones de C++ que se 
usa para comunicarse con el wavelenghtMeter

-----------------------------------------------------------------------------------------------------------------------

Intente en lo posible terminar el programa cerrando la ventana para que la conexión pueda reiniciarse correctamente.

Si el programa termina de otro modo, lo más probable es que tenga que volver a abrir el servidor.

Todos los eventos que ocurren en el programa se imprimen en la terminal.

-----------------------------------------------------------------------------------------------------------------------

Cualquier consulta escribir a azucar.liaf@gmail.com, azulmariabrigante@gmail.com, carovlatko@gmail.com

