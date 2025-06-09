# Práctica de Calculadora Distribuida (SSDD)

Este repositorio contiene la solución para la práctica de la asignatura Sistemas Distribuidos (SSDD) del curso 2024/2025. El objetivo es implementar un servicio de cálculo remoto usando ZeroC Ice y Apache Kafka para la serialización y gestión de operaciones aritméticas básicas.

## Uso del fichero Slice

El fichero Slice (`calculator/remotecalculator.ice`) define la interfaz remota de la calculadora y las excepciones necesarias para la comunicación con ZeroC Ice.

El código que carga el Slice está en el archivo `calculator/__init__.py`. Esto significa que el Slice solo se carga una vez cuando se importa el paquete `calculator` en Python. Gracias a esto, no necesitas cargar el Slice manualmente en cada módulo o submódulo que definas. Esto simplifica el desarrollo y evita errores de carga duplicada.

## Instalación de dependencias

Para instalar las dependencias necesarias, ejecuta:

```sh
pip install .
pip install kafka-python
```

## Configuración y despliegue de Kafka

Para facilitar la ejecución de Kafka, se ha preparado un archivo `docker-compose.yml` que permite levantar el servicio de Kafka de forma sencilla usando Docker.

Crea (si no existe) el archivo `docker-compose.yml` en la raíz del proyecto con el siguiente contenido:

```yaml
version: '3.8'

services:
  kafka:
    container_name: kafka
    image: quay.io/ccxdev/kafka-no-zk:latest
    hostname: kafka
    ports:
      - 9092:9092
    environment:
      - KAFKA_ADVERTISED_HOST_NAME=localhost
      - KAFKA_CREATE_TOPICS=calculator-requests:1:1,calculator-responses:1:1
```

Para iniciar Kafka, ejecuta:

```sh
docker compose up -d
```

Esto levantará un broker Kafka en el puerto 9092 y creará automáticamente los topics `calculator-requests` y `calculator-responses` que utiliza la práctica.

## Configuración del servidor de la calculadora

El endpoint del servidor se configura en el archivo `config/calculator.config`. Por defecto, el contenido es:

```
calculator.Endpoints=tcp -p 10000
```

Puedes cambiar el puerto si lo necesitas.

## Ejecución de la práctica

1. **Inicia Kafka** (si no lo has hecho ya):
   ```sh
   docker compose up -d
   ```

2. **Lanza el servidor de la calculadora:**
   ```sh
   ssdd-calculator --Ice.Config=config/calculator.config
   ```

3. **Lanza el worker de Kafka:**
   ```sh
   kafka-worker
   ```

4. **Prueba el sistema con el script de test:**
   
   He creado el script `test_kafka.py` para realizar el testeo de la práctica. Este script envía automáticamente varias peticiones de operaciones (sumas, restas, multiplicaciones, divisiones, casos con floats, errores de formato... ) al topic de peticiones y muestra por pantalla las respuestas recibidas del topic de respuestas.

   Ejecuta:
   ```sh
   python3 test_kafka.py
   ```
   Verás en consola las respuestas a todas las operaciones y errores, lo que te permite comprobar fácilmente el correcto funcionamiento de toda la práctica.

## Estructura del repositorio

- `calculator/`: Código fuente del servicio de calculadora, worker de Kafka y utilidades.
- `test_kafka.py`: Script de pruebas automáticas para Kafka.
- `config/calculator.config`: Configuración del endpoint del servidor.
- `docker-compose.yml`: Configuración para levantar Kafka con Docker.
- `README.md`: Este archivo.
- `pyproject.toml`: Gestión de dependencias del proyecto.
- `docs/enunciado.md`: Enunciado original de la práctica.

