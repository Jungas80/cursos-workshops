import boto3
import datetime

def evaluate_compliance():
    cloudtrail = boto3.client('cloudtrail')
    
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(days=1)

    # Retrieve CloudTrail events
    event_history = cloudtrail.lookup_events(
        StartTime=start_time,
        EndTime=now,
    )

    # Define your specific event names
    specific_event_names = set(['CreateFunction20150331', 'UpdateFunctionCode20150331v2', 'UpdateFunctionConfiguration20150331v2'])

    # Check for specific event names
    for event in event_history['Events']:
        if event['EventName'] in specific_event_names:
            return 'NON_COMPLIANT'
    
    # If no specific event was found
    return 'COMPLIANT'


def lambda_handler(event, context):
    compliance_type = evaluate_compliance()

    # AWS Config uses the AWS SDK for Python (boto3), to make a call to the 
    # put_evaluations method to report the results of the evaluation of the 
    # compliance of the rule.
    config = boto3.client('config')

    response = config.put_evaluations(
       Evaluations=[
            {
                'ComplianceResourceType': 'AWS::::Account',
                'ComplianceResourceId': '817091419779', 
                'ComplianceType': compliance_type,
                'OrderingTimestamp': datetime.datetime.utcnow()
            },
       ],
       ResultToken=event['resultToken'])

    return response
