Go to Cloudformation and create a new stack using the lambdarole.yml template
Create a new lambda function using python 3.9 runtime and in the permission dropdown select the role you just created with the cloudformation template
Copy the code from email_reminder_lambda.py into the lambda function and deploy it. Copy the ARN of the lambda function and note it down for later