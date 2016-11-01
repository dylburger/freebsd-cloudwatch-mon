from __future__ import print_function
import platform
import psutil


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
