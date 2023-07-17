run this with the credentials of the central id

aws events put-permission --event-bus-name CentralEventBus --action events:PutEvents --principal <CLIENTID>> --statement-id AccountB_Statement --region us-east-1