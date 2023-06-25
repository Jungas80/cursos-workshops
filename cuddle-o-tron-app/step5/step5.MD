Create a new s3 bucket with the name petcuddleotron and some random numbers
Uncheck the block all public access and click Create bucket
Click on the bucket name and then click on the Permissions tab
Edit the bucket policy and paste the static_website_bucket_policy.json content, replacing the bucket name with the name of the bucket you just created
Click Save
Click on the Properties tab and enable Static website hosting
Select Use this bucket to host a website and type index.html for the index document and index.html for the error document. Click Save
Unzip the serverless_frontend.zip file and edit the serverless.js file. Replace the API_URL placeholder with the Invoke URL you copied in the previous step and add /petcuddleotron to the end of the URL
Upload the files to the bucket you created in step 1
Click on the properties tab of the bucket and click on the Static website hosting section. Copy the URL and open it in a new tab
You should see the website and be able to click on the button to start the state machine