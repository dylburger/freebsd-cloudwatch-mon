from __future__ import print_function
import re
import config

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


