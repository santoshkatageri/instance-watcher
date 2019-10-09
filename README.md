# Instance Watcher :eyes:

## Description

This AWS Lambda function will send you once a day a recap email with the list of the running EC2/RDS instances on all AWS region for a giver AWS Account.
I'm using this for non-prod, lab, sandbox, and personal AWS accounts, to get a kindly reminder of what I've left running. :money_with_wings:

## Core features

* List running EC2 instances across all AWS Regions.
  * Check `name`, `instance-id`, `instance_type`, `key_name`, `region`, `launch_time`
* List running RDS instances across all AWS Regions.
  * Check `db_instance_name`, `db_engine`, `db_type`, `db_storage`, `region`, `launch_time`
* White list capability using the `iw` [tag](#Whitelisting)
* Send summary by email once a day
* Serverless Architecture using Lambda, Lambda layer and SES

## Requirements

* [Verify](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses-procedure.html) your sender SES email
* Create `<your_project_name>-artifacts` s3 bucket (default is `instance-watcher-artifacts`)

## Deployment

Change emails settings in `Makefile` or use command-line

> Nb: Recipients are space-delimited

```bash
RECIPIENTS := my_target_email@domain.com my_second_target@domain.com
SENDER := my_source_email@domain.com
```

> You will need to validate email received from AWS SES.

        $ make layer
        $ make package project=<your_project_name>
        $ make deploy \
                ENV=<your_env_name> \
                AWSREGION=<your_aws_region> \
                PROJECT=<your_project_name> \
                SENDER=sender@youremail.com \
                RECIPIENTS='targetemail@youremail.com targetemail2@youremail.com'

*Nb: Use emails in command line is optional if your already setup the `Makefile`*

## Destroy

        $ make tear-down

## Whitelisting

If you want to whitelist a specific EC2 instance to be hidden from the daily report, you will need to add the following tag to the EC2 instance.

| Key | Value |
|:---:|:-----:|
| `iw` | `off` |

## Todo

* Add SES setup built-in
* Whitelist for RDS Instances
* Add unit tests
* Multi-Account Support
* Add `Instance Profile` column
* Add pricing column
