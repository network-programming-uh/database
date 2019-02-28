# Proyecto de Redes de Computadoras

> Base de datos no relacional

## Dependencias

Para que sea más tranquilo el proceso de desarrollo, es recomendable el uso de docker.
Por eso el colectivo de la asignatura les recomienda, fuera de entrar en muchos detalles de la herramienta, que la utilicen.
De cualquier manera, si alguno se interesa por el tema, puede acercarse a cualquiera de los profesores de la asignatura.

No hay ninguna restricción con respecto a las tecnologías a utilizar (menos utilizar directamente otra base de datos ;-))

En caso de necesitar bibliotecas adicionales utilizar una nueva imagen de python. Por defecto la que se utiliza es `python:3.6-alpine`. Ver a los profesores para este tipo de actividad.

## Run tests

Para correr todos los **tests** del proyecto corran:

```
$ docker-compose up
```

La idea es que vean esto:

```
tests_1  | Ran 23 tests in 10.487s
tests_1  | 
tests_1  | OK
```

Si ven algo así:

```
tests_1  | Ran 23 test in 5.341s
tests_1  | 
tests_1  | FAILED (failures=5)
```

busquen dónde están sus errores y corríjanlos.

El proyecto no estará listo hasta que no pasen todos los **tests**.

## Environment

En el archivo `.env` pueden poner todo lo referente a configuración de su servicio, por ejemplo `SERVER_URL`.
Ejemplo para el archivo `.env`:
```sh
$ cat .env
SERVER_URL=db:1234
LOGGING=debug
```

Para acceder a estas variables pueden usar `os.getenv('SERVER_URL')`.

### Variable de entorno `SERVER_URL`

En particular esta variable es utilizada en los tests para instanciar la clase `Client`

 ```python3
 Client(os.getenv('SERVER_URL'))
 ```
La variable debe contener la dirección por la cual el servidor está escuchando. El estudiante es libre de declararla como desee.
Ejemplo:
```
SERVER_URL=http://db:1234/mydb
```
También debe tener en cuenta que Docker le asignará al container donde está corriendo el servicio de la base de datos el nombre de dominio `db`. Por lo que si se declara de la forma
```
SERVER_URL=db:1234
```
implementaciones del tipo
```python3
from socket import socket

class Client(object):
    def __init__(self, server_url):
        host, port = server_url.split(':')
        port = int(port)
        s = socket()
        s.connect((host, port))
```
funcionarán correctamente.
