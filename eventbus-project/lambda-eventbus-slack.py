import json
import urllib3

def lambda_handler(event, context):
    url = ""

    # Extract the relevant fields from the event message
    message_content = json.loads(event['Records'][0]['Sns']['Message'])
    account_id = message_content['detail']['userIdentity']['accountId']
    event_name = message_content['detail'].get('eventName', 'N/A')
    function_arn = message_content['detail']['responseElements']['functionArn']
    last_modified = message_content['detail']['responseElements']['lastModified'].split('.')[0]
    version = message_content['detail']['responseElements']['version']

    # Create a new message with the extracted information
    msg = {
        "channel": "test-slack-notifications",
        "text": f"Account ID: {account_id}\nEvent Name: {event_name}\nFunction ARN: {function_arn}\nLast Modified: {last_modified}\nVersion: {version}",
    }

    http = urllib3.PoolManager()
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST', url, body=encoded_msg)
    print({
        "message": event,
        "status_code": resp.status,
        "response": resp.data
    })

    # Print the message sent to Slack
    print("Message sent to Slack:")
    print(msg)
