import boto3
import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict

cloudtrail_client = boto3.client('cloudtrail')

def lambda_handler(event, context):  # This is the handler function
    # Initialize a dictionary to store the logs
    logs = defaultdict(lambda: defaultdict(list))

    # Process up to 10 messages received from the SQS queue
    for record in event['Records']:
        message_body = json.loads(record['body'])  # Parse the JSON string to a list
        print(f"Message Body: {message_body}")

        for function_name in message_body:  # Iterate over each function name in the list
            # Look up CloudTrail events for the past 24 hours
            start_time = datetime.now(timezone.utc) - timedelta(days=1)
            end_time = datetime.now(timezone.utc)

            paginator = cloudtrail_client.get_paginator('lookup_events')

            for page in paginator.paginate(
                LookupAttributes=[
                    {
                        'AttributeKey': 'ResourceName',
                        'AttributeValue': function_name  # Use the individual function name here
                    },
                ],
                StartTime=start_time,
                EndTime=end_time,
            ):
                # Find the event where the Lambda function was modified
                for event in page['Events']:
                    if 'ModifyFunctionConfiguration' in event['EventName'] or 'UpdateFunctionCode20150331v2' in event['EventName']:
                        # Try to get the user's name from the top level of the event
                        user_name = event.get('Username')

                        # If the 'Username' field is not at the top level of the event, try to get it from the 'userIdentity' field
                        if user_name is None:
                            user_identity = event.get('userIdentity', {})
                            if 'sessionContext' in user_identity:
                                user_name = user_identity['sessionContext']['sessionIssuer']['userName']
                            else:
                                user_name = user_identity.get('userName')

                        # If the user's name is still None at this point, set it to 'Unknown'
                        if user_name is None:
                            user_name = 'Unknown'

                        # Add the log to the dictionary
                        logs[function_name][user_name].append(event['EventTime'])

    # Print the logs
    for function_name, users in logs.items():
        print(f"Function Name: {function_name}")
        for user_name, times in users.items():
            print(f"Modified By: {user_name}")
            for time in times:
                print(f"Time: {time}")
            print(f"Total Modifications: {len(times)}")
        print("--------------------------")

    return {
        'statusCode': 200,
        'message': "Processed SQS messages and checked CloudTrail logs."
    }
