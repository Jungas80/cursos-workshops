import boto3
from datetime import datetime, timezone

lambda_client = boto3.client('lambda')

def lambda_handler(event, context):  # This is the handler function
    current_date = datetime.now(timezone.utc).date()  # get current date

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
                modified_today.append(version['FunctionName'])  # Add the function name to the list

    return {
        'statusCode': 200,
        'body': modified_today  # Return the list of function names
    }
