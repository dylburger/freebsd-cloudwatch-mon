# FreeBSD CloudWatch Monitor

Collect metrics from a FreeBSD system, push to Amazon CloudWatch.

The [scripts](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mon-scripts.html) Amazon provides to poll metrics for Linux systems uses [procfs](https://en.wikipedia.org/wiki/Procfs), which has been [deprecated on FreeBSD](https://lists.freebsd.org/pipermail/freebsd-fs/2011-February/010760.html). 

This code helps fill that gap, monitoring CPU, Memory, Disk and Network metrics on FreeBSD using pure Python.

### Requirements

* Python >= 2.7
* Modules listed in requirements.txt

### Usage

    from MetricsMonitor import MetricsMonitor, Metric, CloudWatchClient
    c = CloudWatchClient()
    mm = MetricsMonitor()
    m = Metric('MemoryUtilization', mm.get_memory_utilization(), 'Percent')
    c.put_metric_data(m.data)
