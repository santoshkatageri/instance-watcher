# EC2 Instance Watcher

## Description

This AWS Lambda function will send you once a day an email with the list of the running EC2 instances on all AWS region for an AWS Account.

## Core features

* [ ] List running EC2 instances accross all AWS Regions
* [ ] Check `instance-id`, `instance_type`, `region`
* [ ] Send summuary by email once a day
* [ ] Serverless Architecture using Lambda and Lambda layer

## Requirements

* Verified SES email (sender)
* Create `instance-watcher-<your_project>-artifacts` s3 bucket

## Deployment

change emails settings in `handlers.py`

```
# Email Settings
recipients = ['ops@company.com', 'you@company.com']
subject = '[AWS] Instance Watcher - '
sender = 'Instance Watcher <ops@company.com>'
charset = "UTF-8"
```
        $ make layer
        $ make package
        $ make deploy

## Todo

* Add EC2 Launch time Column
* Add RDS Instances table
* Add Detached EBS table
* Add Detached EIP table

## Info

- https://stackoverflow.com/questions/38924348/send-formatted-html-email-via-aws-ses-with-python-and-boto3
- https://stackoverflow.com/questions/44062367/amazon-ses-with-flask-python
