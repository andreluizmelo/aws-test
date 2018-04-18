# André Luiz Melo' portfolio
This is an AWS test for my potential portfolio.
It will use AWS and ReactJS.

## AWS Setup
Code Pipeline watches github and triggers a Code Build event (which only compiles the less file for now). On success, a Lambda function is called to unzip the result and place the compiled contents in the S3 bucket that is used to serve the content. Cloud Front and Route 53 are also used to serve the bucket through HTTPS and a more friendly address.

## Technologies used
Less for a better CSS;
Python for the AWS Lambda function;
React(not yet actually, comming in the next days/commits)


## Photos
Photos were taken from Pexels, a website where you can get pictures under the CC0 license.