import boto3
import json, gzip
from datetime import datetime

from elasticsearch import Elasticsearch

# Get the service resource
sqs = boto3.resource('sqs', region_name='us-east-1')
s3 = boto3.client('s3')

elasticsearch_base_url = 'elasticsearch-apps-client.elasticsearch.svc.cluster.local'
es = Elasticsearch([{'host': elasticsearch_base_url, 'port': 9200}])

# Get the queue
queue = sqs.get_queue_by_name(QueueName='concerto')

# print('Starting to push concerto notifications to elasticsearch')

i=0

while True:
    response = queue.receive_messages(
        WaitTimeSeconds=20, MaxNumberOfMessages=1)
    i+=1

    # Process messages by printing out body
    for message in response:
        timestamp = str(datetime.now())
        message_id = json.loads(message.body)["MessageId"]

        log = {
            "timestamp": timestamp,
            "processing_message": message_id,
            "loop": i
        }

        print(log)

        notification = json.loads(json.loads(message.body)["Message"])
        sns_timestamp = json.loads(message.body)["Timestamp"]
        notification["SNS_Timestamp"] = sns_timestamp
        es.index(index="concerto-notifications", doc_type='record', id=message_id, body=notification)

        print(json.loads(json.loads(message.body)["Message"]))
        message.delete()
    