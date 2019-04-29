# EC2 Instance Watcher

## Description

This lambda function will send you once a day an email with the list of the running EC2 instances on all AWS region for a defined AWS Account.

## Core features

* [ ] List running EC2 instances accross all AWS Regions
* [ ] Check `instance-id`, `instance_type`, `region`, `launch_time`
* [ ] Send summuary by email once a day
* [ ] Serverless Architecture

## Requierements

* Verified SES email
* Create `instance-watcher-artifacts` s3 bucket

## Deployment

change emails settings in `handlers.py`

```
# Email Settings
recipients = ['ops@company.com', 'you@company.com']
subject = '[AWS] Instance Watcher - '
sender = 'Instance Watcher <victor.grenu@gmail.com>'
charset = "UTF-8"
```

        $ make package
        $ make deploy

## Todo

* Add RDS Instances
* Add Detached EBS
* Add Detached EIP
* Automate SES email verification

## Info

- https://stackoverflow.com/questions/38924348/send-formatted-html-email-via-aws-ses-with-python-and-boto3
- https://stackoverflow.com/questions/44062367/amazon-ses-with-flask-python
