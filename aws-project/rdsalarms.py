import boto3
import json
import random
import string

client_cw = boto3.client('cloudwatch')

alarm_name = ""
alarm_desc = ""
ok_actions = []
alarm_actions = []
metric_name = ""
namespace = ""
dimensions = []

def create_alarm(alarm_name, description, ok_actions, alarm_actions, metric_name, namespace,
                 threshold, comparison, dimensions):
    response = client_cw.put_metric_alarm(
        AlarmName = alarm_name,
        AlarmDescription = description,
        ActionsEnabled=True,
        OKActions=ok_actions,
        AlarmActions=alarm_actions,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic='Average',
        Dimensions=dimensions,
        Period=300,
        EvaluationPeriods=1,
        DatapointsToAlarm=1,
        Threshold=threshold,
        ComparisonOperator=comparison,
        TreatMissingData='missing',
        # EvaluateLowSampleCountPercentile='string',
        # Metrics=[
        #     {
        #         'Id': 'string',
        #         'MetricStat': {
        #             'Metric': {
        #                 'Namespace': 'string',
        #                 'MetricName': 'string',
        #                 'Dimensions': [
        #                     {
        #                         'Name': 'string',
        #                         'Value': 'string'
        #                     },
        #                 ]
        #             },
        #             'Period': 123,
        #             'Stat': 'string',
        #             'Unit': 'Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'
        #         },
        #         'Expression': 'string',
        #         'Label': 'string',
        #         'ReturnData': True|False,
        #         'Period': 123,
        #         'AccountId': 'string'
        #     },
        # ],
    )
    print(response)
    return

# ComparisonOperator='GreaterThanOrEqualToThreshold'|'GreaterThanThreshold'|'LessThanThreshold'|'LessThanOrEqualToThreshold'|'LessThanLowerOrGreaterThanUpperThreshold'|'LessThanLowerThreshold'|'GreaterThanUpperThreshold',
# database = 'mysql57-public'
# database = 'mysql57-public-2'
# database = 'aurora-public-1'
# database = 'aurora-public-2'
#database = 'tbmstaging5731'
database = 'tbmprod'
# database = 'mysql-8'
# database = 'mysql-8b'


# sns_arn = "arn:aws:sns:us-east-1:065738303452:CrowdWisdomNRA-CloudOpsAlerts"
sns_arn = "arn:aws:sns:us-east-1:495738975186:TBM-RDS-ALERTS"

#RDS-mysql57-public-select-latency-alert
alarm_name = f"RDS-{database}-latency-alert"
alarm_desc = f"Select latency on {database} database is higher than defined threshold."
ok_actions = [sns_arn]
alarm_actions = [sns_arn]
metric_name = "SelectLatency"
namespace = "AWS/RDS"
threshold = 2000 
comparison = "GreaterThanThreshold"
dimensions = [
    {
        "Name": "DBInstanceIdentifier",
        "Value": f"{database}"
    }
]
create_alarm(alarm_name, alarm_desc, ok_actions, alarm_actions, metric_name, namespace, 
             threshold, comparison, dimensions)


# RDS-mysql57-public-available-storage alert
alarm_name = f"RDS-{database}-available-FreeStorageSpace"
alarm_desc = f"Available storage on {database} database is less than defined threshold"
#metric_name = "FreeLocalStorage"
metric_name = "FreeStorageSpace"
threshold = 10000000000  
comparison = "LessThanOrEqualToThreshold"
create_alarm(alarm_name, alarm_desc, ok_actions, alarm_actions, metric_name, namespace, 
             threshold, comparison, dimensions)


# RDS-mysql57-public-available-memory-alert
alarm_name = f"RDS-{database}-available-memory-alert"
alarm_desc = f"Available memory for {database} database is lower than defined threshold."
metric_name = "FreeableMemory"
threshold =  214748364.8
comparison = "LessThanOrEqualToThreshold"
create_alarm(alarm_name, alarm_desc, ok_actions, alarm_actions, metric_name, namespace, 
             threshold, comparison, dimensions)


# RDS-mysql57-public-CPU-alert
alarm_name = f"RDS-{database}-CPU-alert"
alarm_desc = f"CPU utilization on {database} database is higher than defined threshold."
metric_name = "CPUUtilization"
threshold = 90    
comparison = "GreaterThanThreshold"
create_alarm(alarm_name, alarm_desc, ok_actions, alarm_actions, metric_name, namespace, 
             threshold, comparison, dimensions)

