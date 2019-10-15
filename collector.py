import boto3
from prometheus_client.core import GaugeMetricFamily, Summary
import logging


class Logger:
    """Class used to display logs on the console.
    """

    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        self.logger = logger


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


class CloudwatchLogsCollector:
    """Class used to get metrics from AWS Cloudwatch Logs.
    """

    def __init__(self):
        self.client = boto3.client('logs')
        self.metric_prefix = "aws_logs_"
        self.logger = Logger().logger

    @REQUEST_TIME.time()
    def collect_log_groups(self):
        log_group_stored_byte = GaugeMetricFamily(
            self.metric_prefix + 'stored_bytes',
            'Total size of the log group in bytes',
            labels=['log_group_name']
        )
        paginator = self.client.get_paginator('describe_log_groups')
        pages = paginator.paginate()
        for page in pages:
            for object in page['logGroups']:
                log_group_stored_byte.add_metric([object['logGroupName']], object['storedBytes'])
        return log_group_stored_byte

    def collect(self):
        self.logger.info("Collect metrics")
        yield self.collect_log_groups()
