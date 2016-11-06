""" Poll system data, send to CloudWatch
"""
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
    cfg = config.YAMLParser(config.CONFIG_FILE).config

    @classmethod
    def get_namespace(cls):
        return cls.cfg['cloudwatch_namespace']

    def __init__(self):
        self.client = boto3.client('cloudwatch')
        self.namespace = self.get_namespace()

    def put_metric_data(self, metric_data):
        self.client.put_metric_data(Namespace=self.namespace, MetricData=metric_data)


class MetricsMonitor(object):
    """ Wraps the psutil module to easily extract FreeBSD
        system metrics
    """
    def __init__(self, metric_type):
        self.platform = platform.platform()
        self.metric_type = metric_type

    def __repr__(self):
        return 'MetricsMonitor(%r)' % (self.platform)

    def poll(self, **kwargs):
        """ Given a metric type, poll for the underlying metric
        """
        if self.metric_type == 'memory_utilization':
            return self.get_memory_utilization()
        elif self.metric_type == 'disk_usage':
            try:
                return self.get_disk_space(partition=kwargs['partition'])
            except:
                raise ValueError("It's possible you failed to pass the "
                                 "'partition' argument to this method. kwargs: %s" % kwargs)
        else:
            raise ValueError("Couldn't poll for metric type '%s'" % self.metric_type)

    def get_memory_utilization(self):
        return psutil.virtual_memory().percent

    def get_disk_space(self, partition):
        try:
            return psutil.disk_usage(partition).percent
        except OSError:
            print("The partition %s you passed doesn't appear to exist" % partition)


class Metric(object):
    """ Class to hold CloudWatch metric dictionaries,
        to be POSTed to AWS by a CloudwatchClient
    """
    def __init__(self, metric_type):
        # Given a metric type, grab the metric name and units from config file
        try:
            cfg = config.YAMLParser(config.CONFIG_FILE).config['metrics'][metric_type]
            self.metric_name = cfg['metric_name']
            self.units = cfg['unit']
        except KeyError:
            print("Failed to find a metric with the specific metric_type.",
                  "Please check / add your metric to %s" % config.CONFIG_FILE)
        # Instantiate the object where we store our metric data
        metric_data = []
        metric_data.append({})
        d = metric_data[0]
        d['MetricName'] = self.metric_name
        d['Unit'] = self.units
        d['Value'] = 0
        self.data = metric_data

        # We need a metric monitor to poll for data
        self.metric_monitor = MetricsMonitor(metric_type)
        # ... and a client to PUT data to CloudWatch
        self.cloudwatch_client = CloudWatchClient()

    def __repr__(self):
        return 'Metric(%r)' % (self.data)

    def update(self, **kwargs):
        """ Update the Value of our metric stored as an attribute
            PUT data to CloudWatch
        """
        value = self.metric_monitor.poll(**kwargs)
        self.data[0]['Value'] = value
        # PUT data to CloudWatch
        self.cloudwatch_client.put_metric_data(self.data)
        print("Successfully PUT value %s %s to metric %s in CloudWatch"
              % (value, self.units, self.metric_name))
