import boto3
from prometheus_client.core import GaugeMetricFamily
import logging
import time


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


class CloudwatchLogsCollector:
    """Class used to get metrics from AWS Cloudwatch Logs.
    """

    def __init__(self):
        self.client = boto3.client('logs')
        self.metric_prefix = "aws_logs_"
        self.logger = Logger().logger
        self.metric_collector_duration = None

    def collect_log_groups(self):
        start = time.time()
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
        end = time.time()
        self.metric_collector_duration.add_metric(['log_groups'], end-start)
        return log_group_stored_byte

    def collect(self):
        self.logger.info("Collect metrics")
        self.metric_collector_duration = GaugeMetricFamily(
            self.metric_prefix + 'collector_duration_seconds',
            'Duration of a collection', labels=['collector'])

        yield self.collect_log_groups()
        yield self.metric_collector_duration
