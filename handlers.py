import boto3

AWS_REGION = 'eu-west-1'
session = boto3.Session(region_name=AWS_REGION)
ec2 = session.client('ec2')
ses = session.client('ses')
sts = session.client('sts')

# Email Settings
# export to external file or aws parameter store
recipients = ['victor.grenu@gmail.com']
subject = '[AWS] Instance Watcher 👀 - '
sender = 'Instance Watcher <victor.grenu@gmail.com>'
charset = "UTF-8"

def main(event, context):
    # Activate mail notifications
    mail_enabled = 1
    running_ec2 = []
    running_rds = []
    hidden_count = 0
    #hidden_rds_count = 0
    account = sts.get_caller_identity().get('Account')
    alias = boto3.client('iam').list_account_aliases()['AccountAliases'][0]
    ec2_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    # For all AWS Regions
    for region in ec2_regions:
        print("Checking running instances in: " + region)
        
        # RDS Checking
        rdscon = boto3.client('rds', region_name=region)
        rds = rdscon.describe_db_instances()
        for r in rds['DBInstances']:
            db_instance_name = r['DBInstanceIdentifier']
            db_engine =  r['Engine']
            db_type = r['DBInstanceClass']
            db_storage = r['AllocatedStorage']
            db_creation_time = r['InstanceCreateTime'].strftime("%Y-%m-%d %H:%M:%S")
            db_publicly_accessible = r['PubliclyAccessible']

            running_rds.append({
                "db_instance_name": r['DBInstanceIdentifier'],
                "db_engine": r['Engine'],
                "db_type": r['DBInstanceClass'],
                "db_storage": r['AllocatedStorage'],
                "db_publicly_accessible": r['PubliclyAccessible'],
                "region": region,
                "launch_time": r['InstanceCreateTime'].strftime("%Y-%m-%d %H:%M:%S")
            })
            print(db_instance_name,db_engine,db_type,db_storage,db_creation_time,db_publicly_accessible)
        
        # EC2 Checking
        ec2con = boto3.resource('ec2', region_name=region)
        instances = ec2con.instances.filter()
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
                    running_ec2.append({
                        "instance_name": instancename,
                        "id": instance.id,
                        "instance_type": instance.instance_type,
                        "key_pair": instance.key_name,
                        "region": region,
                        "launch_time": instance.launch_time.strftime("%Y-%m-%d %H:%M:%S")
                    })
            else:
                print("- No running instance, but some exist (Pending, Stopped or Terminated)")
    print("Total number of running EC2 instance(s):", len(running_ec2))
    print("Total number of hidden EC2 instance(s):", hidden_count)
    print("Total number of running RDS instance(s):", len(running_rds))
    #print("Total number of hidden RDS instance(s):", len(hidden_rds_count)) # not yet implemented

# do a function
    if (len(running_ec2) == 0 and len(running_rds) == 0):
        print("Nothing to do here, no running EC2 or RDS instances")
    else:
        if mail_enabled == 1:
            print("Sending email to: " + str(recipients))
            body_text = (
                        """
                        Instance Watcher\r\n
                        Running EC2 Instances {ec2}
                        Running RDS Instances {rds}
                        """).format(
                                ec2=len(running_ec2),
                                rds=len(running_rds),
                            )
            header = """
            <html>
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
                    <p>AWS AccountID: <a href="https://""" + account + """.signin.aws.amazon.com/console">""" + account + """</a> - <a href=https://""" + alias + """.signin.aws.amazon.com/console>""" + alias + """</a></p>"""
            
            # Crafting EC2 html table
            if len(running_ec2) > 0:
                ec2_table = """
                    <h3>Running EC2 Instances: </h3>
                    <table cellpadding="4" cellspacing="4">
                    <tr><td><strong>Name</strong></td><td><strong>Instance ID</strong></td><td><strong>Intsance Type</strong></td><td><strong>Key Name</strong></td><td><strong>Region</strong></td><td><strong>Launch Time</strong></td></tr>
                    """ + \
                        "\n".join([f"<tr><td>{r['instance_name']}</td><td>{r['id']}</td><td>{r['instance_type']}</td><td>{r['key_pair']}</td><td>{r['region']}</td><td>{r['launch_time']}</td></tr>" for r in running]) \
                        + """
                    </table>
                    <p>Total number of running EC2 instance(s): """ + str(len(running_ec2)) + """
                    <br />Total number of hidden EC2 instance(s): """ + str(hidden_count) + """</p>"""
            else:
                ec2_table = """"""
            
            # Crafting RDS html table
            if len(running_rds) > 0:
                rds_table = """
                    <h3>Running RDS Instances: </h3>
                    <table cellpadding="4" cellspacing="4">
                    <tr><td><strong>Name</strong></td><td><strong>Engine</strong></td><td><strong>DB Type</strong></td><td><strong>Volume (GB)</strong></td><td><strong>Region</strong></td><td><strong>Launch Time</strong></td></tr>
                    """ + \
                        "\n".join([f"<tr><td>{r['db_instance_name']}</td><td>{r['db_engine']}</td><td>{r['db_type']}</td><td>{r['db_storage']}</td><td>{r['region']}</td><td>{r['launch_time']}</td></tr>" for r in running_rds]) \
                        + """
                    </table>
                    <p>Total number of running RDS instance(s): """ + str(len(running_rds)) + """"""
            else:
                rds_table = """"""
            
            footer = """
                    <p><a href="https://github.com/z0ph/instance-watcher">Instance Watcher 🖤</a></p>
                </body>
            </html>
            """
            # Concatenate html email
            body_html = header + ec2_table + rds_table + footer

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
