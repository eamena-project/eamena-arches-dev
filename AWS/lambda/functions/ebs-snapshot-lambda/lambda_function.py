# copied from AWS/EAMENA the 22-09-26
# runtime: Python 2.7

import boto3
import collections
import datetime
import logging
import sys

logger = logging.getLogger()
for h in logger.handlers:
  logger.removeHandler(h)

h = logging.StreamHandler(sys.stdout)
FORMAT = ' [%(levelname)s]/%(asctime)s/%(name)s - %(message)s'
h.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(h)
logger.setLevel(logging.INFO)

ec = boto3.client('ec2')

def lambda_handler(event, context):

    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag:EBS_Backup', 'Values': ['Yes', 'yes']},
        ]
    ).get(
        'Reservations', []
    )

    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    logger.info("Number of instances that need ebs backing = %d" % len(instances))

    to_tag = collections.defaultdict(list)

    for instance in instances:
        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'EBS_Snapshot_Retention'][0]
        except IndexError:
            retention_days = 7

        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None or dev['DeviceName']=='/dev/sda1':
                continue
            vol_id = dev['Ebs']['VolumeId']
            logger.info("Found EBS volume %s on instance %s" % (
                vol_id, instance['InstanceId']))
            try:
                snap = ec.create_snapshot(
                    VolumeId=vol_id,Description='Snapshot_'+datetime.datetime.now().strftime('%m-%d-%Y')+'_'+str(instance['InstanceId'])
                )
                ec2 = boto3.resource('ec2')
                snapshot=ec2.Snapshot(snap['SnapshotId'])
                snapshot.create_tags(Tags=[
                    {
                        'Key': 'Name',
                        'Value': 'Snapshot_'+vol_id
                        },
                        ])
                logger.info("Instance-id:%s, Volume-id:%s, Snapshot-id:%s,Snapshot-size:%s" % (instance['InstanceId'],vol_id,snap['SnapshotId'],snap['VolumeSize']))
                to_tag[retention_days].append(snap['SnapshotId'])
            except Exception as e:
                logger.error("Error occured:",e)
            
            logger.info("Retaining snapshot %s of volume %s from instance %s for %d days" % (
                snap['SnapshotId'],
                vol_id,
                instance['InstanceId'],
                retention_days,
            ))
    
    
    for retention_days in to_tag.keys():
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        delete_fmt = delete_date.strftime('%Y-%m-%d')
        logger.info("Will delete %d snapshots on %s" % (len(to_tag[retention_days]), delete_fmt))
        ec.create_tags(
            Resources=to_tag[retention_days],
            Tags=[
                {'Key': 'DeleteOn', 'Value': delete_fmt},
            ]
        )