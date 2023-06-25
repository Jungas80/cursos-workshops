Go to Cloudformation and create a new stack using the StateMachineRole.yml template
Go to step functions and create a new state machine. Select the option "Write your workflow in code" and  use the StateMachine.json template in the definition
Replace the FunctionArn in the definition with the ARN of the lambda function you created in the previous step and click Next
In tge Define state machine settings page, enter PetCuddleOTron for the state machine
In permissions, select the role you created in the previous step and click Next
In the logging section dropdown, select ALL and click Create state machine
Copy the ARN of the state machine and note it down for later