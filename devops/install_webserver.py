#!/usr/bin/python
import docker
from util import timer

stopwatch = timer.Stopwatch()

print 'hello world'

stopwatch.output_report()