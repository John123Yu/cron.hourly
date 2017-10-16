import sys
import os
import time
from datetime import datetime

file_name = '/var/log/harvester_run.log'
current_time = datetime.now()

harvester_run_log = open(file_name, 'r').readlines()
harvester_run_log_tail = harvester_run_log[-30:-1]
harvester_run_log_last_line = harvester_run_log[-2:-1][0]

for line in harvester_run_log_tail:
    print line
print harvester_run_log_last_line

print "CURRENT TIME"
print current_time

try:
    mtime = os.path.getmtime(file_name)
except OSError:
    mtime = 0
last_modified = datetime.fromtimestamp(mtime)

print "file last modified"
print last_modified

print "Time difference"
time_difference_hours = (current_time - last_modified).total_seconds() / 3600
print time_difference_hours

if time_difference_hours > .02:
    print "MORE"
else:
    print "LESS"

