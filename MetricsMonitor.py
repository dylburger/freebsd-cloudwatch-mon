from __future__ import print_function
import platform
import boto3
import psutil
import config


class CloudWatchClient(object):
    """ Handles connection and POSTing of metrics data
        to CloudWatch
    """
    # Our config is shared across all Metrics
    config = config.YAMLParser(config.CONFIG_FILE)

    def __init__(self):
        self.client = boto3.client('cloudwatch')
        self.namespace = config.cloudwatch_namespace

    def put_metric_data(self, metric_data):
        self.client.put_metric_data(Namespace=self.namespace, MetricData=metric_data)


class MetricsMonitor(object):
    """ Wraps the psutil module to easily extract FreeBSD
        system metrics
    """
    def __init__(self):
        self.platform = platform.platform()

    def __repr__(self):
        return 'MetricsMonitor(%r)' % (self.platform)

    def get_memory_utilization(self):
        return psutil.virtual_memory().percent

    def get_disk_space(self, partition):
        try:
            return psutil.disk_usage(partition)
        except OSError:
            print("The partition %s you passed doesn't appear to exist" % partition)


class Metric(object):
    """ Class to hold CloudWatch metric dictionaries,
        to be POSTed to AWS by a CloudwatchClient
    """
    def __init__(self, metric_name, value, unit):
        metric_data = []
        metric_data.append({})
        d = metric_data[0]
        d['MetricName'] = metric_name
        d['Value'] = value
        d['Unit'] = unit
        self.data = metric_data

    def __repr__(self):
        return 'Metric(%r)' % (self.data)
