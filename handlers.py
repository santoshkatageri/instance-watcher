import boto3

AWS_REGION = 'eu-west-1'
session = boto3.Session(region_name=AWS_REGION)
ec2 = session.client('ec2')
ses = session.client('ses')
sts = session.client('sts')

# Email Settings
recipients = ['victor.grenu@gmail.com']
subject = '[AWS] Instance Watcher 👀 - '
sender = 'Instance Watcher <victor.grenu@gmail.com>'
charset = "UTF-8"


def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def main(event, context):
    running = []
    account = sts.get_caller_identity().get('Account')
    ec2_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    for region in ec2_regions:
        conn = boto3.resource('ec2', region_name=region)
        print("Checking running instances in: " + region)
        instances = conn.instances.filter()
        for instance in instances:
            if instance.state["Name"] == "running":
                for tags in instance.tags:
                    if tags["Key"] == 'Name':
                        instancename = tags["Value"]
                print(instancename, instance.id, instance.instance_type, instance.key_name, region, instance.launch_time.strftime("%Y-%m-%d %H:%M:%S"))
                running.append({
                    "instance_name": instancename,
                    "id": instance.id,
                    "instance_type": instance.instance_type,
                    "key_pair": instance.key_name,
                    "region": region,
                    "launch_time": instance.launch_time.strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                print("No running instance, but some exist (Stopped, Terminated)")
    print("Total number of running instance(s):", len(running))

    if len(running) == 0:
        print("Nothing to do here, no running EC2")
    else:
        print("Sending email to: " + str(recipients))
        body_text = ("Instance Watcher\r\n"
                     "Running EC2 Instances" + str(split(running, 3))
                     )
        body_html = """<html>
        <body>
        <h1>Instance Watcher 👀</h1>
        <p>AWS AccountID: <a href="https://""" + account + """.signin.aws.amazon.com/console">""" + account + """</a></p>
        <h3>Running EC2 Instances: </h3>
        <table cellpadding="4" cellspacing="4" border="1">
        <tr><td><strong>Name</strong></td><td><strong>Instance ID</strong></td><td><strong>Intsance Type</strong></td><td><strong>Key Name</strong></td><td><strong>Region</strong></td><td><strong>Launch Time</strong></td></tr>
        """ + \
            "\n".join([f"<tr><td>{r['instance_name']}</td><td>{r['id']}</td><td>{r['instance_type']}</td><td>{r['key_pair']}</td><td>{r['region']}</td><td>{r['launch_time']}</td></tr>" for r in running]) \
            + """
        </table>
        <p>Total number of running instance(s): """ + str(len(running)) + """</p>
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


#main(0, 0)
