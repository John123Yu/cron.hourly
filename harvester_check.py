import sys
import os
import time
from datetime import datetime

datetime_chars = {str(x) for x in range(0,10)}
additional_datetime_chars = ['-', ' ', ':']
for char in additional_datetime_chars:
    datetime_chars.add(char)

harvester_run_log = open('/var/log/harvester_run.log', 'r').readlines()
harvester_run_log_tail = harvester_run_log[-30:-1]
harvester_run_log_last_line = harvester_run_log[-2:-1][0]
#current_time = time.time()
#current_time = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
current_time = datetime.now()
for line in harvester_run_log_tail:
    print line
#print harvester_run_log_tail
print harvester_run_log_last_line

last_timestamp = ""
for char in harvester_run_log_last_line:
    if char in datetime_chars:
        last_timestamp += char
    else:
        break

print datetime_chars
print last_timestamp
print current_time
time_difference = current_time - datetime.strptime(last_timestamp, '%Y-%m-%d %H:%M:%S')
print time_difference
