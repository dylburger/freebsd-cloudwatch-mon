# FreeBSD CloudWatch Monitor

**This is still a work in progress and should not be used to monitor production systems**

**What does this do?**

Polls memory utilization, CPU usage, and other systems metrics for FreeBSD, pushing them to [CloudWatch](https://aws.amazon.com/cloudwatch/).

**Why this tool?**

The [scripts](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mon-scripts.html) Amazon provides to push metrics for Linux systems to CloudWatch uses [procfs](https://en.wikipedia.org/wiki/Procfs), which has been [deprecated on FreeBSD](https://lists.freebsd.org/pipermail/freebsd-fs/2011-February/010760.html). 

**Can I use it on Linux or other systems?**

In theory, this will work on any architecture on which [psutil](https://github.com/giampaolo/psutil) is configured to work, but this tool has been tested on FreeBSD only.

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

to add your AWS access and secret keys you created above to a config file, which we'll use to push metrics to your account.

### Usage

When creating a new CloudWatch metric, you have the option to define your own [namespace](http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-namespaces.html). We've defined a default namespace tied to all metrics in `config.yml`.

All metrics are also configured in `config.yml`, each with a Metric Name (tied to your metric in CloudWatch) and the Units tied to the metric value:

	metrics:
		memory_utilization:
			metric_name: "MemUtilization"
			unit: "Percent"
		disk_usage:
			metric_name: "DiskUsage"
			unit: "Percent"

Here's an example of how you can push memory utilization and disk usage stats to CloudWatch:

	>>> from CloudWatchMonitor import Metric
	>>> mm = Metric('memory_utilization')
	>>> mm.update()
	Successfully PUT value 75.2 Percent to metric MemUtilization in CloudWatch
	>>> dm = Metric('disk_usage')
	>>> dm.update(partition='/')
	Successfully PUT value 23.5 Percent to metric DiskUsage in CloudWatch

