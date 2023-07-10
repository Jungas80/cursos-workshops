import boto3
import json
from datetime import datetime, timedelta
from collections import defaultdict

cloudtrail_client = boto3.client('cloudtrail')

def lambda_handler(event, context):
    
    start_time = datetime.now() - timedelta(days=1)
    end_time = datetime.now()

    event_names = ['CreateFunction20150331', 'UpdateFunctionCode20150331v2', 'UpdateFunctionConfiguration20150331v2'] # Upgrade 1: Feed this input from a dynamodb table for easier maintenance

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
                # Extract the resources affected by the event
                for resource in event.get('Resources', []):
                    resource_name = resource.get('ResourceName')
                    if resource_name:
                        # Add the event to the list of events for this resource
                        resource_logs[resource_name].append(event)

    create_function_events = defaultdict(list)
    update_function_code_events = defaultdict(list)
    update_function_configuration_events = defaultdict(list)

    # Print the logs for each resource
    for resource_name, events in resource_logs.items():
        for event in events:
            if event['EventName'] == 'CreateFunction20150331':
                # Store the event for later printing
                create_function_events[resource_name].append(event)
            elif event['EventName'] == 'UpdateFunctionCode20150331v2':
                # Store the event for later printing
                update_function_code_events[resource_name].append(event)
            elif event['EventName'] == 'UpdateFunctionConfiguration20150331v2':
                # Store the event for later printing
                update_function_configuration_events[resource_name].append(event)
            else:
                print(f"Resource: {resource_name}")
                print(json.dumps(event, default=str))

    # Print the 'CreateFunction20150331' events per resource
    for resource_name, events in create_function_events.items():
        print(f"These Lambda Functions were created today: {resource_name}")
        for event in events:
            event_time = event['EventTime']
            user_name = event['Username']
            print(f"  Created at: {event_time}, by user: {user_name}")

    # Print the 'UpdateFunctionCode20150331v2' events per resource
    for resource_name, events in update_function_code_events.items():
        print(f"These Lambda Functions were updated today: {resource_name}")
        for event in events:
            event_time = event['EventTime']
            user_name = event['Username']
            print(f"  Updated at: {event_time}, by user: {user_name}")

    # Print the 'UpdateFunctionConfiguration20150331v2' events per resource
    for resource_name, events in update_function_configuration_events.items():
        print(f"These Lambda Functions were reconfigured today: {resource_name}")
        for event in events:
            event_time = event['EventTime']
            user_name = event['Username']
            print(f"  Reconfigured at: {event_time}, by user: {user_name}")
