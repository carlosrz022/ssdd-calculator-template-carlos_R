"""Kafka worker for remote calculator microservice."""
import json
import sys
import os
from kafka import KafkaConsumer, KafkaProducer
import Ice

import RemoteCalculator  # pylint: disable=import-error

slice_path = os.path.join(os.path.dirname(__file__), "remotecalculator.ice")
Ice.loadSlice(slice_path)

KAFKA_BROKER = 'localhost:9092'  # Cambia si es necesario
REQUEST_TOPIC = 'calculator-requests'
RESPONSE_TOPIC = 'calculator-responses'

# Opcional: puedes mover la configuración a un archivo aparte

def validate_request(msg):
    """Valida el formato del mensaje de petición según el enunciado."""
    if not isinstance(msg, dict):
        return False, 'not a dict'
    if 'id' not in msg or not isinstance(msg['id'], str):
        return False, 'missing or invalid id'
    if 'operation' not in msg or msg['operation'] not in ('sum', 'sub', 'mult', 'div'):
        return False, 'invalid or missing operation'
    if 'args' not in msg or not isinstance(msg['args'], dict):
        return False, 'missing or invalid args'
    if 'op1' not in msg['args'] or 'op2' not in msg['args']:
        return False, 'missing operands'
    try:
        float(msg['args']['op1'])
        float(msg['args']['op2'])
    except Exception:
        return False, 'operands must be float'
    return True, None

def build_response(req_id, status, result=None, error=None):
    """Construye la respuesta según el formato del enunciado."""
    response = {
        'id': req_id,
        'status': status
    }
    if status:
        response['result'] = result
    else:
        response['error'] = error
    return response

def main():
    """Main function to start the Kafka worker for the remote calculator service."""
    with Ice.initialize(sys.argv) as communicator:
        proxy = communicator.stringToProxy('calculator:tcp -p 10000')
        calculator = RemoteCalculator.CalculatorPrx.checkedCast(proxy)
        if not calculator:
            print('No se pudo obtener el proxy del servicio Calculator')
            sys.exit(1)
        consumer = KafkaConsumer(
            REQUEST_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            value_deserializer=lambda m: m.decode('utf-8'),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='calculator-worker-group',
        )
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )
        print('Kafka worker started. Waiting for messages...')
        for msg in consumer:
            try:
                data = json.loads(msg.value)
            except json.JSONDecodeError:
                continue
            req_id = data.get('id', None)
            valid, reason = validate_request(data)
            if not valid:
                if req_id:
                    response = build_response(
                        req_id, False, result=None, error=f'format error: {reason}'
                    )
                    producer.send(RESPONSE_TOPIC, response)
                continue
            op = data['operation']
            op1 = float(data['args']['op1'])
            op2 = float(data['args']['op2'])
            try:
                if op == 'sum':
                    result = calculator.sum(op1, op2)
                elif op == 'sub':
                    result = calculator.sub(op1, op2)
                elif op == 'mult':
                    result = calculator.mult(op1, op2)
                elif op == 'div':
                    try:
                        result = calculator.div(op1, op2)
                    except RemoteCalculator.ZeroDivisionError:
                        response = build_response(
                            data['id'], False, result=None,
                            error="operation error: Cannot divide by zero"
                        )
                        producer.send(RESPONSE_TOPIC, response)
                        continue
                else:
                    response = build_response(
                        data['id'], False, result=None, error="operation not found"
                    )
                    producer.send(RESPONSE_TOPIC, response)
                    continue
                response = build_response(data['id'], True, result=result)
            except (ValueError, TypeError) as e:
                response = build_response(data['id'], False, result=None, error=str(e))
            producer.send(RESPONSE_TOPIC, response)
# pylint: disable=too-many-return-statements, too-many-locals