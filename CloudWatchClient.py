import boto3
import config


class CloudWatchClient(object):
    """ Handles connection and POSTing of metrics data
        to CloudWatch
    """
    # Our config is shared across all Metrics
    cfg = config.YAMLParser(config.CONFIG_FILE).config

    @classmethod
    def get_namespace(cls):
        return cls.cfg['cloudwatch_namespace']

    def __init__(self):
        self.client = boto3.client('cloudwatch')
        self.namespace = self.get_namespace()

    def put_metric_data(self, metric_data):
        self.client.put_metric_data(Namespace=self.namespace, MetricData=metric_data)
