from MetricsMonitor import MetricsMonitor


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

        # We need a metric monitor to poll for data
        self.metric_monitor = MetricsMonitor()

    def __repr__(self):
        return 'Metric(%r)' % (self.data)

    def update_metric_value(self, value):
        """ Update the Value of our metric stored as an attribute
        """
        self.data[0]['Value'] = value


class MemoryMetric(Metric):
    """ Sublass to handle memory metrics
    """
    def __init__(self, metric_name="MemUtilization", value=0, unit="Percent"):
        Metric.__init__(self, metric_name, value, unit)

    def poll(self):
        """ Poll for memory, returning data
        """
        memory_utilization = self.metric_monitor.get_memory_utilization()
        super(MemoryMetric, self).update_metric_value(memory_utilization)
        return self.data


class DiskUsageMetric(Metric):
    """ Sublass to handle disk usage metrics for a particular partition
    """
    def __init__(self, partition, metric_name="MemUtilization", value=0, unit="Percent"):
        Metric.__init__(self, metric_name, value, unit)
        self.partition = partition

    def poll(self):
        """ Poll for disk usage, returning data
        """
        disk_usage = self.metric_monitor.get_disk_space(self.partition)
        super(DiskUsageMetric, self).update_metric_value(disk_usage)
        return self.data
