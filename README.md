# Proyecto de Redes de Computadoras

> Base de datos no relacional

## Dependencias

Para que sea más tranquilo el proceso de desarrollo, es recomendable el uso de docker.
Por eso el colectivo de la asignatura les recomienda, fuera de entrar en muchos detalles de la herramienta, que la utilicen.
De cualquier manera, si alguno se interesa por el tema, puede hacercarse a cualquiera de los profesores de la asignatura.

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
```
$ cat .env
SERVER_URL=db:1234
LOGGING=debug
```

Para acceder a estas variables pueden usar `os.getenv('SERVER_URL')`.
