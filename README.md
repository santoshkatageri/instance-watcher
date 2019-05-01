# EC2 Instance Watcher :eyes:

## Description

This AWS Lambda function will send you once a day a recap email with the list of the running EC2 instances on all AWS region for a giver AWS Account.
I'm using this for nonprod, lab, and personal AWS accounts, to get a kindly reminder of what I've left running.

## Core features

* List running EC2 instances accross all AWS Regions
* Check `name`, `instance-id`, `instance_type`, `key_name`, `region`, `launch_time`
* Send summuary by email once a day
* Serverless Architecture using Lambda, Lambda layer, SES

## Requirements

* [Verify](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html) your sender SES email
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
        $ make deploy project=<your_project>

## Todo

* Create input file for settings or param store (recipients, sender, etc..)
* Add RDS Instances table
* Add Detached EBS table
* Add Detached EIP table
* Multi-Account Support
