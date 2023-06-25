Create a new lambda function using python 3.9 runtime called api_lambda assing the execution role created in the step 2 (the same from email_reminder) and paste the code from api_lambda.py
Replace the SM_ARN placeholder with the ARN of the state machine you created in the previous step
Copy the ARN of the lambda function and note it down for later
Go to API Gateway and create a new API. Select REST API and click Build
Select New API and give it the name petcuddleotron. Select Regional and then Click Create API
Click Actions and select Create Resource. Give it the name petcuddleotron select Enable API Gateway CORS (DO NOT CHECK THE PROXY RESOURCE) and click Create Resource
Click Actions and select Create Method. Select POST and click the checkmark
Select Lambda Function and check the box Use Lambda Proxy integration. Select the region where you created the lambda function and type the name of the lambda function you created in the previous step. It should be api_lambda. Click Save
Click Actions and select Deploy API. Select [New Stage] and give it the name prod. Click Deploy
Copy the Invoke URL and note it down for later
