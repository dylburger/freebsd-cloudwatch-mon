# FreeBSD CloudWatch Monitor

Collect system metrics from a FreeBSD system, push to Amazon CloudWatch.

The [scripts](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mon-scripts.html) Amazon provides to poll metrics for Linux systems uses [procfs](https://en.wikipedia.org/wiki/Procfs), which has been [deprecated on FreeBSD](https://lists.freebsd.org/pipermail/freebsd-fs/2011-February/010760.html). 

This code helps fill that gap, monitoring CPU, Memory, Disk and Network metrics on FreeBSD using pure Python. In theory, this will work on any architecture on which [psutil](https://github.com/giampaolo/psutil) is configured to work, but this code has been tested on FreeBSD only.

### AWS Requirements

To push metrics to CloudWatch, you'll first want to [create an IAM role](http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html) with permission to perform the following operations:

* cloudwatch:PutMetricData
* cloudwatch:GetMetricStatistics
* cloudwatch:ListMetrics
* ec2:DescribeTags

Keep the secret and access keys in a secure place - you'll use them in the section below.

### System Requirements

First, ensure Python >= 2.7 is installed. Run

    python -V

to confirm. Next, it's recommended that you install:

* [pip](https://pip.pypa.io/en/stable/installing/)
* [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation)

After installation, create a new virtual environment:

    mkvirtualenv aws-freebsd-mon

and install the necessary modules:

    pip install -r requirements.txt

Finally, run

    aws configure

to add your AWS access and secret keys you created above to a config file this program can read.

### Usage

When creating a new CloudWatch metric, you have the option to define your own [namespace](http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-namespaces.html). The default, custom namespace we define here can be found in _config.yml_. This namespace is used when pushing metrics to CloudWatch, but can be overridden on a metric-by-metric basis (see the _put\_metric\_data_ method in the _CloudWatchClient_ class).

There are a handful of classes we've defined:

* _CloudWatchClient_ : Handles the connection to AWS, and the PUT requests to CloudWatch
* _MetricsMonitor_ : Polls the FreeBSD server for data
* _Metric_ : Abstracts the creation of a [put\_metric\_data](http://boto3.readthedocs.io/en/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_data) request object to be passed to our _CloudWatchClient_

Here's an example of how you can push memory utilization to CloudWatch:

    from MetricsMonitor import MetricsMonitor, Metric, CloudWatchClient
    c = CloudWatchClient()
    mm = MetricsMonitor()
    m = Metric('MemoryUtilization', mm.get_memory_utilization(), 'Percent')
    c.put_metric_data(m.data)
