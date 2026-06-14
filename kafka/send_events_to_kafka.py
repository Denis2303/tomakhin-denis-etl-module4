import os
import sys
from pathlib import Path
from kafka import KafkaProducer

if len(sys.argv) < 2:
    raise ValueError('Usage: send_events_to_kafka.py <jsonl_path>')

jsonl_path = Path(sys.argv[1])
bootstrap_servers = os.environ['KAFKA_BOOTSTRAP_SERVERS'].split(',')
topic = os.environ.get('KAFKA_TOPIC', 'loan-applications')
security_protocol = os.environ.get('KAFKA_SECURITY_PROTOCOL', 'SASL_SSL')
sasl_mechanism = os.environ.get('KAFKA_SASL_MECHANISM', 'SCRAM-SHA-512')
username = os.environ.get('KAFKA_USERNAME')
password = os.environ.get('KAFKA_PASSWORD')

kwargs = {
    'bootstrap_servers': bootstrap_servers,
    'value_serializer': lambda value: value.encode('utf-8')
}

if username and password:
    kwargs.update({
        'security_protocol': security_protocol,
        'sasl_mechanism': sasl_mechanism,
        'sasl_plain_username': username,
        'sasl_plain_password': password
    })

producer = KafkaProducer(**kwargs)
count = 0

with jsonl_path.open('r', encoding='utf-8') as file:
    for line in file:
        value = line.strip()
        if value:
            producer.send(topic, value=value)
            count += 1
            if count % 1000 == 0:
                producer.flush()
                print(count)

producer.flush()
producer.close()
print(count)
