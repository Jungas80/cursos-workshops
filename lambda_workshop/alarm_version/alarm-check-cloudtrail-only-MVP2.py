import boto3
import json
from datetime import datetime, timedelta
from collections import defaultdict

cloudtrail_client = boto3.client('cloudtrail')
sqs_client = boto3.client('sqs')
sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/817091419779/MyQueue'  # Replace with your SQS Queue URL

def lambda_handler(event, context):
    start_time = datetime.now() - timedelta(days=1)
    end_time = datetime.now()

    event_names = ['CreateFunction20150331', 'UpdateFunctionCode20150331v2', 'UpdateFunctionConfiguration20150331v2']

    resource_logs = defaultdict(list)

    paginator = cloudtrail_client.get_paginator('lookup_events')

    for event_name in event_names:
        response_iterator = paginator.paginate(
            LookupAttributes=[
                {'AttributeKey': 'EventName', 'AttributeValue': event_name},
            ],
            StartTime=start_time,
            EndTime=end_time,
        )

        for page in response_iterator:
            for event in page['Events']:
                for resource in event.get('Resources', []):
                    resource_name = resource.get('ResourceName')
                    if resource_name:
                        resource_logs[resource_name].append(event)

    total_events = {
        'CreateFunction20150331': [],
        'UpdateFunctionCode20150331v2': [],
        'UpdateFunctionConfiguration20150331v2': []
    }

    for resource_name, events in resource_logs.items():
        for event in events:
            event_info = {
                'resource': resource_name,
                'time': str(event['EventTime']), 
                'user': event['Username'],
                'eventId': event['EventId'],  # Include the EventId in your output
            }
            if event['EventName'] == 'CreateFunction20150331':
                total_events['CreateFunction20150331'].append(event_info)
                print(f"Function {resource_name} was created at {event_info['time']} by {event_info['user']} with EventId {event_info['eventId']}")
            elif event['EventName'] == 'UpdateFunctionCode20150331v2':
                total_events['UpdateFunctionCode20150331v2'].append(event_info)
                print(f"Function {resource_name} was updated at {event_info['time']} by {event_info['user']} with EventId {event_info['eventId']}")
            elif event['EventName'] == 'UpdateFunctionConfiguration20150331v2':
                total_events['UpdateFunctionConfiguration20150331v2'].append(event_info)
                print(f"Function {resource_name} was reconfigured at {event_info['time']} by {event_info['user']} with EventId {event_info['eventId']}")



    # Convert the total_events dictionary to a JSON string
    json_message = json.dumps(total_events)

    # Send the JSON message to the SQS queue
    sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=json_message)
