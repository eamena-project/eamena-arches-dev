# copied from AWS/EAMENA the 22-09-26
# runtime: Python 2.7

import boto3
from datetime import datetime
import re
import logging
import sys
import re
import time;
import random

localtime = time.asctime( time.localtime(time.time()) )
logger = logging.getLogger()
for h in logger.handlers:
  logger.removeHandler(h)

h = logging.StreamHandler(sys.stdout)
FORMAT = ' [%(levelname)s]/%(asctime)s/%(name)s - %(message)s'
h.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(h)
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    logs = boto3.client('logs')
    ebs_logGroupName='/aws/lambda/ebs-snapshot-lambda'
    ami_logGroupName='/aws/lambda/ami-image-lambda'
    Report="Backup Report,"+localtime+"\n\n"
    #get ebs snapshot log streams
    try:
        ebs_response = logs.describe_log_streams(
        logGroupName=ebs_logGroupName)
    except Error as e:
        logger.error("No log stream found for EBS snapshot"+e)
        ebs_response=None
    
    #get ami image log streams
    try:
        ami_response = logs.describe_log_streams(
        logGroupName=ami_logGroupName)
    except Error as e:
        logger.error("No log stream found for AMI image"+e)
        ami_response=None
    s3 = boto3.client('s3')
    #move ebs snapshot logs to s3
    if ebs_response is not None:
        for i in ebs_response["logStreams"]:
            data=i["logStreamName"]
            ebs_log_events = logs.get_log_events(logGroupName=ebs_logGroupName,
            logStreamName=data)
            s3.put_object(Bucket='ebs-snapshot-cw-logs-eamena',Key=data+'.json',Body=str(ebs_log_events))
            logs.delete_log_stream(logGroupName=ebs_logGroupName,logStreamName=data)
            f=-1
            try:
                for _event in ebs_log_events['events']:
                    msg=_event['message']
                    m = re.match( r'.*?Number of instances that need ebs backing = (.*)', msg.strip())
                    if m:
                        Report+="\n\nNumber of instances for EBS Snapshot,"+m.group(1)+"\n\n"
                        continue
                    m = re.match( r'\[INFO\]/(.*?) (.*?)\,.*/.*?Instance-id:(.*?), Volume-id:(.*?), Snapshot-id:(.*),Snapshot-size:(.*)', msg.strip())
                    if m:
                        if f==-1:
                            Report+="Creation Date,Creation Time,Instance-ID,Volume-ID,Snapshot-ID,Snapshot-size\n"
                            f=0
                        Report+=m.group(1)+","+m.group(2)+","+m.group(3)+","+m.group(4)+","+m.group(5)+","+m.group(6)+"\n"
                        continue
                    m = re.match( r'.*?Will delete (.*?) snapshots on (.*)', msg.strip())
                    if m:
                        Report+="\nSnapshot deletion date,"+m.group(2)+"\n"
                        continue
            except:
                Report+="\n\nNumber of instances for EBS Snapshot,0"+"\n\n"
        logger.info(str(len(ebs_response["logStreams"]))+" ebs snapshot logs moved to S3")
        #move ami image logs to S3
    if ami_response is not None:
        try:
            for i in ami_response["logStreams"]:
                data=i["logStreamName"]
                ami_log_events = logs.get_log_events(logGroupName=ami_logGroupName,
                logStreamName=data)
                s3.put_object(Bucket='ami-image-cw-logs-eamena',Key=data+'.json',Body=str(ami_log_events))
                logs.delete_log_stream(logGroupName=ami_logGroupName,logStreamName=data)
            logger.info(str(len(ami_response["logStreams"]))+" ami image logs moved to S3")
            f=-1
            for _event in ami_log_events['events']:
                msg=_event['message']
                m = re.match( r'.*?Number of instances to create AMI = (.*)', msg.strip())
                if m:
                    Report+="\n\nNumber of instances for AMI image,"+m.group(1)+"\n\n"
                    continue
                m = re.match( r'\[INFO\]/(.*?) (.*?)\,.*/.*?Instance-id=(.*?) Image-id=(.*)', msg.strip())
                if m:
                    if f==-1:
                        Report+="Creation Date,Creation Time,Instance-ID,Image-ID\n"
                        f=0
                    Report+=m.group(1)+","+m.group(2)+","+m.group(3)+","+m.group(4)+"\n"
                    continue
                m = re.match( r'.*?Number of AMIs to be deleted on (.*?) = .*', msg.strip())
                if m:
                    Report+="\nAMI deletion date,"+m.group(1)+"\n"
                    continue
        except:
            Report+="\n\nNumber of instances for AMI image,0"+"\n\n"
    # Report generation
    Report = Report.encode('utf-8')
    _keyname=str(localtime)
    _keyname=_keyname.replace(" ","")
    _keyname=_keyname.replace(":","")
    r=s3.put_object(Body=Report,Bucket='backup-reports-eamena',Key=str(random.randint(1, 100000000))+"_"+_keyname+".csv")
    print(r)