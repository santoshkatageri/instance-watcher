# EC2 Instance Watcher :eyes:

## Description

This AWS Lambda function will send you once a day an email with the list of the running EC2 instances on all AWS region for a giver AWS Account.

## Core features

* [ ] List running EC2 instances accross all AWS Regions
* [ ] Check `name`, `instance-id`, `instance_type`, `key_name`, `region`, `launch_time`
* [ ] Send summuary by email once a day
* [ ] Serverless Architecture using Lambda, Lambda layer, SES

## Requirements

* Verified SES email (sender)
* Create `<your_project>-artifacts` s3 bucket (default is instance-watcher)

## Deployment

change emails settings in `handlers.py`

```
# Email Settings
recipients = ['ops_team@company.com', 'you@company.com']
subject = '<your email subject>'
sender = 'Instance Watcher <ops@company.com>'
charset = "UTF-8"
```
        $ make layer
        $ make package project=<your_project>
        $ make deploy

## Todo

* Add RDS Instances table
* Add Detached EBS table
* Add Detached EIP table
* Multi-Account Support
