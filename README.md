# Instance Watcher :eyes:

## Description

This AWS Lambda function will send you once a day a recap email with the list of the running EC2 instances on all AWS region for a giver AWS Account.
I'm using this for non-prod, lab, and personal AWS accounts, to get a kindly reminder of what I've left running.

## Core features

* List running EC2 instances across all AWS Regions.
  * Check `name`, `instance-id`, `instance_type`, `key_name`, `region`, `launch_time`
* List running RDS instances across all AWS Regions.
  * Check `db_instance_name`, `db_engine`, `db_type`, `db_storage`, `region`, `launch_time`
* Filter / White list capability using a tag
* Send summary by email once a day
* Serverless Architecture using Lambda, Lambda layer, SES

## Requirements

* [Verify](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html) your sender SES email
* Create `<your_project>-artifacts` s3 bucket (default is instance-watcher)

## Deployment

Change emails settings in `handlers.py`

```bash
# Email Settings
recipients = ['ops_team@company.com', 'you@company.com']
subject = '<your email subject>'
sender = 'Instance Watcher <ops@company.com>'
charset = "UTF-8"
```

> You will need to validate email received from AWS SES.

        $ make layer
        $ make package project=<your_project>
        $ make deploy project=<your_project>

## Whitelisting

If you want to whitelist a specific EC2 instance to be hidden from the daily report, you will need add the following tag to the EC2 instance.

| Key | Value |
|:---:|:-----:|
| `iw` | `off` |

## Todo

* Create input file for settings or param store (recipients, sender, etc..)
* Add RDS Instances table
* Multi-Account Support
* Add instance role column
