# OldDante

Dante was a slack bot written with python using the RTM api by a former colleague.
In an effort to re-familiarize myself with some aws concepts, I decided to create this 
read-only version using Lambda, SSM, S3 and AWS-CDK. It's not perfect but it does the job.

Uses Slack Events API via Api Gateway to trigger lambda to generate the response.
Response is generated by reading the last known markov state then calling the slack api.
Slack tokens are read from SSM and the markov state is read from S3.

Next steps would be to produce the lambda zip and call CDK deploy 
from inside GH actions as well as npm testing.