import boto3
from datetime import datetime, timezone
import json

lambda_client = boto3.client('lambda')
sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    current_date = datetime.now(timezone.utc).date()

    paginator = lambda_client.get_paginator('list_functions')
    function_names = []

    for page in paginator.paginate():
        for function in page['Functions']:
            function_names.append(function['FunctionName'])
        
    modified_today = []  # List to store the names of functions modified today

    for function_name in function_names:
        response = lambda_client.list_versions_by_function(FunctionName=function_name)
        
        for version in response['Versions']:
            last_modified = datetime.strptime(version['LastModified'], "%Y-%m-%dT%H:%M:%S.%f%z")

            # Compare dates
            if last_modified.date() == current_date:
                modified_today.append(version['FunctionName'])
    # Prepare the message
    if modified_today:
        message = "These Lambda functions were modified today!"
        # Send a single message to the SQS queue with all modified functions
        sqs_client.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/817091419779/alarm-version-queue',  # Replace with your queue URL
            MessageBody=json.dumps(modified_today),  # Convert list to JSON string
        )
    else:
        message = "No Lambda functions were modified today."

    output = {
        'statusCode': 200,
        'message': message,
        'modifiedFunctions': modified_today  # Return the list of function names
    }

    print(output)

    return output
