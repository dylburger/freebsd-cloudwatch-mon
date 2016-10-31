from __future__ import print_function
import boto3

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
