# calculator repository template

Template for the extra SSDD laboratory 2024-2025

## Installation

To locally install the package, just run

```
pip install .
```

Or, if you want to modify it during your development,

```
pip install -e .
```

## Execution

To run the template server, just install the package and run

```
ssdd-calculator --Ice.Config=config/calculator.config
```

## Configuration

This template only allows to configure the server endpoint. To do so, you need to modify
the file `config/calculator.config` and change the existing line.

For example, if you want to make your server to listen always in the same TCP port, your file
should look like

```
calculator.Endpoints=tcp -p 10000
```

## Slice usage

The Slice file is provided inside the `calculator` directory. It is only loaded once when the `calculator`
package is loaded by Python. It makes your life much easier, as you don't need to load the Slice in every module
or submodule that you define.

The code loading the Slice is inside the `__init__.py` file.

## Ejecución completa y pruebas

### 1. Instalar dependencias

```sh
pip install .
pip install kafka-python
```

### 2. Levantar Zookeeper y Kafka (en Docker)

```sh
docker run -d --name zookeeper -p 2181:2181 zookeeper:3.4.9
docker run -d --name kafka -p 9092:9092 \
  -e KAFKA_ZOOKEEPER_CONNECT=172.17.0.1:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
  wurstmeister/kafka
```
> Cambia la IP `172.17.0.1` si tu docker0 tiene otra.

### 3. Ejecutar el servidor de la calculadora

```sh
ssdd-calculator --Ice.Config=config/calculator.config
```

### 4. Ejecutar el worker de Kafka

```sh
kafka-worker
```

### 5. Probar el sistema

```sh
python3 test_kafka.py
```

Verás en consola las respuestas a todas las operaciones y errores.
