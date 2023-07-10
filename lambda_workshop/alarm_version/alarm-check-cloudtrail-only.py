import boto3
import datetime
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    client = boto3.client('cloudtrail')
    current_time = datetime.datetime.now()
    start_time = current_time - datetime.timedelta(days=1)

    lambda_events = []
    paginator = client.get_paginator('lookup_events')
    
    response_iterator = paginator.paginate(
        LookupAttributes=[
            {'AttributeKey': 'EventName', 'AttributeValue': 'CreateFunction20150331'},
            {'AttributeKey': 'EventName', 'AttributeValue': 'UpdateFunctionCode20150331v2'},
            {'AttributeKey': 'EventName', 'AttributeValue': 'UpdateFunctionConfiguration'},
            {'AttributeKey': 'EventName', 'AttributeValue': 'UpdateAlias'},
            {'AttributeKey': 'EventName', 'AttributeValue': 'PutFunctionConcurrency'},
            {'AttributeKey': 'EventName', 'AttributeValue': 'DeleteFunctionConcurrency'},
        ],
        StartTime=start_time,
        EndTime=current_time,
    )

    for response in response_iterator:
        for event in response['Events']:
            request_params = json.loads(event['CloudTrailEvent']).get('requestParameters', {})
            lambda_function_name = request_params.get('functionName')
            event_info = {
                'event_time': str(event['EventTime']),
                'user_name': event['Username'],
                'lambda_function': lambda_function_name,
            }
            lambda_events.append(event_info)

    # Log the event information to CloudWatch Logs
    for event in lambda_events:
        logger.info(event)

    return {
        'statusCode': 200,
        'body': json.dumps(lambda_events)
    }
