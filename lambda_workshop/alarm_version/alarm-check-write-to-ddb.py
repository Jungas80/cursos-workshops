import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('alarm-version-output')  # Replace with your table name 

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])

        # Flatten the json
        for event_name, events in body.items():
            for event in events:
                try:
                    table.put_item(
                        Item={
                            'resource': event['resource'],
                            'time': event['time'],
                            'user': event['user'],
                            'eventName': event_name,
                            'eventId': event['eventId'],
                        }
                    )
                except ClientError as e:
                    print(e.response['Error']['Message'])
                else:
                    print("PutItem succeeded")
