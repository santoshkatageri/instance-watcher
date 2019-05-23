import boto3

AWS_REGION = 'eu-west-1'
session = boto3.Session(region_name=AWS_REGION)
ec2 = session.client('ec2')
ses = session.client('ses')
sts = session.client('sts')

# Email Settings
# export to external file or aws parameter store
recipients = ['victor.grenu@external.engie.com']
subject = '[AWS] Instance Watcher 👀 - '
sender = 'Instance Watcher <victor.grenu@external.engie.com>'
charset = "UTF-8"

def main(event, context):
    # Activate mail notifications
    mail_enabled = 1
    running = []
    hidden_count = 0
    account = sts.get_caller_identity().get('Account')
    alias = boto3.client('iam').list_account_aliases()['AccountAliases'][0]
    ec2_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    # For all AWS Regions
    for region in ec2_regions:
        conn = boto3.resource('ec2', region_name=region)
        print("Checking running instances in: " + region)
        instances = conn.instances.filter()
        # For every instances in region
        for instance in instances:
            if instance.state["Name"] == "running":
                # For all instances tags
                for tags in instance.tags:
                    hidden = 0
                    if tags["Key"] == 'Name':
                        instancename = tags["Value"]
                    if tags["Key"] == 'iw' and tags["Value"] == 'off':
                        hidden = 1
                        hidden_count = +1
                        break
                if hidden != 1:
                    print(instancename, instance.id)
                    # fill the list
                    running.append({
                        "instance_name": instancename,
                        "id": instance.id,
                        "instance_type": instance.instance_type,
                        "key_pair": instance.key_name,
                        "region": region,
                        "launch_time": instance.launch_time.strftime("%Y-%m-%d %H:%M:%S")
                    })
            else:
                print("- No running instance, but some exist (Pending, Stopped or Terminated)")
    print("Total number of running instance(s):", len(running))
    print("Total number of hidden instance(s):", hidden_count)

# do a function
    if len(running) == 0:
        print("Nothing to do here, no running EC2")
    else:
        if mail_enabled == 1:
            print("Sending email to: " + str(recipients))
            body_text = ("Instance Watcher\r\n"
                        "Running EC2 Instances" + str(len(running))
                        )
            body_html = """<html>
            <head>
            <style>
                table, th, td {
                border: 3px solid black;
                border-collapse: collapse;
                }
            </style>
            </head>
            <body>
            <h1>Instance Watcher 👀</h1>
            <p>AWS AccountID: <a href="https://""" + account + """.signin.aws.amazon.com/console">""" + account + """</a> - <a href=https://""" + alias + """.signin.aws.amazon.com/console>""" + alias + """</a></p>
            <h3>Running EC2 Instances: </h3>
            <table cellpadding="4" cellspacing="4">
            <tr><td><strong>Name</strong></td><td><strong>Instance ID</strong></td><td><strong>Intsance Type</strong></td><td><strong>Key Name</strong></td><td><strong>Region</strong></td><td><strong>Launch Time</strong></td></tr>
            """ + \
                "\n".join([f"<tr><td>{r['instance_name']}</td><td>{r['id']}</td><td>{r['instance_type']}</td><td>{r['key_pair']}</td><td>{r['region']}</td><td>{r['launch_time']}</td></tr>" for r in running]) \
                + """
            </table>
            <p>Total number of running instance(s): """ + str(len(running)) + """
            <br />Total number of hidden instance(s): """ + str(hidden_count) + """</p>
            <p><a href="https://github.com/z0ph/instance-watcher">Instance Watcher 🖤</a></p>
            </body>
            </html>
            """
            response = ses.send_email(
                Destination={
                    'ToAddresses': recipients,
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': charset,
                            'Data': body_html,
                        },
                        'Text': {
                            'Charset': charset,
                            'Data': body_text,
                        },
                    },
                    'Subject': {
                        'Charset': charset,
                        'Data': subject + account,
                    },
                },
                Source=sender,
            )
            print("Email sent! Message ID:"),
            print(response['MessageId'])

if __name__ == '__main__':
    main(0,0)
