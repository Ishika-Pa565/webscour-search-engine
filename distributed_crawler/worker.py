import pika # type: ignore
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import os
from urllib.parse import urlparse

# Create folder if not exists
folder_name = "pages"
os.makedirs(folder_name, exist_ok=True)

MAX_PAGES = 5
count = 0
visited = set()

def callback(ch, method, properties, body):
    global count

    url = body.decode()

    #  Stop if limit reached
    if count >= MAX_PAGES:
        print("Limit Reached. Stopping Worker.")
        ch.stop_consuming()
        return

    #  Skip already visited URLs
    if url in visited:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    visited.add(url)
    print("Processing:", url)

    try:
        response = requests.get(url, timeout=5)
        html = response.text

        # Create safe filename using urlparse
        parsed_url = urlparse(url)
        safe_filename = parsed_url.netloc + parsed_url.path
        safe_filename = safe_filename.replace("/", "_")

        if safe_filename == "":
            safe_filename = "index"

        filename = os.path.join(folder_name, safe_filename + ".html")

        #  Save HTML file inside pages folder
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

        print("Saved:", filename)

        soup = BeautifulSoup(html, "html.parser")

        #  Publish new links
        if count < MAX_PAGES:
            for link in soup.find_all("a", href=True):
                new_url = link['href']
                if new_url.startswith("http") and new_url not in visited:
                    ch.basic_publish(
                        exchange='',
                        routing_key='url_queue',
                        body=new_url
                    )

        count += 1
        print("Pages Crawled:", count)

    except Exception as e:
        print("Error:", e)

    ch.basic_ack(delivery_tag=method.delivery_tag)


# RabbitMQ Connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()
channel.queue_declare(queue='url_queue')

channel.basic_consume(
    queue='url_queue',
    on_message_callback=callback
)

print("Worker Started...")
channel.start_consuming()
