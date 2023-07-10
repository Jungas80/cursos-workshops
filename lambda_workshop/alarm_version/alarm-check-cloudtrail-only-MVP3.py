## This lambda function checks CloudTrail logs for specific events and sends a message to an SQS queue ##
# if the event is not present in the CloudTrail logs for the last 24 hours #
## Created by Juan Hegert - DevOps Engineer ##

import os
import boto3
import json
from datetime import datetime, timedelta
from collections import defaultdict
from dateutil import parser

cloudtrail_client = boto3.client('cloudtrail')
sqs_client = boto3.client('sqs')
sqs_queue_url = (os.environ.get('SQS_QUEUE_URL')) # This should be a variable created in the CloudFormation template and passed in as an environment variable - Juan)  # This should be a variable created in the CloudFormation template and passed in as an environment variable - Juan
lookback_hours = int(os.environ.get('LOOKBACK_HOURS', '1')) # '1' is the default value if the environment variable is not set - Juan

def lambda_handler(event, context):
    
    start_time = datetime.now() - timedelta(hours=lookback_hours)
    end_time = datetime.now()

    event_names = ['CreateFunction20150331', 'UpdateFunctionCode20150331v2', 'UpdateFunctionConfiguration20150331v2'] # In a next iteration, this could be dynamically passed in as an environment variable - Juan

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
            # Parse the 'CloudTrailEvent' JSON string to a dictionary
            details = json.loads(event['CloudTrailEvent'])

            # Extract the accountId from the 'userIdentity' dictionary
            accountId = details['userIdentity']['accountId'] if 'userIdentity' in details and 'accountId' in details['userIdentity'] else None

            # Format 'EventTime' as a string without the timezone information
            formatted_time = event['EventTime'].strftime('%Y-%m-%d %H:%M:%S')

            event_info = {
                'accountId': accountId,  
                'resource': resource_name,
                'time': formatted_time, 
                'user': event['Username'],
                'eventId': event['EventId'] 
            }
            if event['EventName'] == 'CreateFunction20150331':
                total_events['CreateFunction20150331'].append(event_info)
                print(f"Function {resource_name} was created at {event_info['time']} by {event_info['user']} with EventId {event_info['eventId']} in Account {accountId}")
            elif event['EventName'] == 'UpdateFunctionCode20150331v2':
                total_events['UpdateFunctionCode20150331v2'].append(event_info)
                print(f"Function {resource_name} was updated at {event_info['time']} by {event_info['user']} with EventId {event_info['eventId']} in Account {accountId}")
            elif event['EventName'] == 'UpdateFunctionConfiguration20150331v2':
                total_events['UpdateFunctionConfiguration20150331v2'].append(event_info)
                print(f"Function {resource_name} was reconfigured at {event_info['time']} by {event_info['user']} with EventId {event_info['eventId']} in Account {accountId}")


    # Convert the total_events dictionary to a JSON string
    json_message = json.dumps(total_events)

    # Send the JSON message to the SQS queue
    sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=json_message)
