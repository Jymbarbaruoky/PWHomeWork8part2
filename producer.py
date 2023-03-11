from datetime import datetime
import json

from models import MessageInfo

import pika
from faker import Faker

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')


def create_db_records():
    for i in range(10):
        mi = MessageInfo(fullname=fake.name(), email=fake.email(), message=fake.text()).save()


def create_tasks():
    mes = MessageInfo.objects()
    for m in mes:
        message = {
            "id": str(m.id),
            "message": m.message,
        }

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    connection.close()

def main():
    create_db_records()
    create_tasks()


if __name__ == '__main__':
    main()
