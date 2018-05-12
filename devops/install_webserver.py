#!/usr/bin/python
from infrastructure import platform_aws as provider
from util import multi_thread
from util import ssh
from util import timer

stopwatch = timer.Stopwatch()



stopwatch.output_report()