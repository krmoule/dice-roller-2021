import json
import base64

from google.cloud import pubsub_v1

project_id = 'dice-roller-2021'
topic_id = 'discord-deferred'

batch_settings = pubsub_v1.types.BatchSettings(
    max_messages=1,     # default 100
    max_bytes=10240,    # default 1 MB
    max_latency=0.001,  # default 10 ms
)
publisher = pubsub_v1.PublisherClient(batch_settings)

# Send |message| to the deferred pubsub topic for
# further processing. |message| is expected to be a
# dict that can be turned into json, containing
# 'token', 'user' and 'skill'.
def send_deferred(message):
    global publisher
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(message).encode('utf-8')
    future = publisher.publish(topic_path, data)
    print(future.result())
    print(f'Published {message} to {topic_path}.')

# Decode the message received in the deferred function,
# returning same |message| that would have been handed
# to send_deferred.
def decode(data):
    return json.loads(base64.b64decode(data).decode('utf-8'))

if __name__ == '__main__':
    send_deferred({
        'token': 'test-token',
        'user': 'test-user',
        'skill': 'test-skill'
    })