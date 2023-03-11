import json
from random import randint

from models import ClientInfo

import pika
from faker import Faker

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_email', exchange_type='direct')
channel.queue_declare(queue='email_task_queue', durable=True)
channel.queue_bind(exchange='task_email', queue='email_task_queue')

channel.exchange_declare(exchange='task_sms', exchange_type='direct')
channel.queue_declare(queue='sms_task_queue', durable=True)
channel.queue_bind(exchange='task_sms', queue='sms_task_queue')


def create_db_records():
    for i in range(10):
        ClientInfo(fullname=fake.name(), email=fake.email(), phone=fake.phone_number(),
                    best_message_is_email=bool(randint(0, 1))).save()


def create_tasks(message_to: str):
    mes = ClientInfo.objects()
    for m in mes:
        message = {
            "id": str(m.id),
            "message": message_to,
        }

        if m.best_message_is_email:
            channel.basic_publish(
                exchange='task_email',
                routing_key='email_task_queue',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            print(" [x] Sent %r" % message)
        else:
            channel.basic_publish(
                exchange='task_sms',
                routing_key='sms_task_queue',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            print(" [x] Sent %r" % message)
    connection.close()


def main():
    mes = input('Enter the message: ')
    create_db_records()
    create_tasks(mes)


if __name__ == '__main__':
    main()
