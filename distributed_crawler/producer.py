import pika # type: ignore

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()

channel.queue_declare(queue='url_queue')

# Times of India as seed URL
seed_url = "https://timesofindia.indiatimes.com/"

channel.basic_publish(
    exchange='',
    routing_key='url_queue',
    body=seed_url
)

print("Seed URL Sent!")

connection.close()
