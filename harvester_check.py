import os
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from email import Utils

file_name = '/var/log/harvester_run.log'
current_time = datetime.now()
_ERRORS = False
recipient_emails = ['john.yu@reisystems.com', 'john123yu@gmail.com']
mail_from = 'no-reply@data.gov'
message_body = "Hello World"

harvester_run_log = open(file_name, 'r').readlines()
harvester_run_log_tail = harvester_run_log[-30:-1]
harvester_run_log_last_line = harvester_run_log[-2:-1][0]

def _send_mail(mail_from='', recipient_emails=[''],
        msg=MIMEText(''.encode('utf-8'), 'plain', 'utf-8')):
    # Send the email using Python's smtplib.
    smtp_connection = smtplib.SMTP()
    smtp_connection.connect('localhost')
    try:
        smtp_connection.ehlo()
        smtp_connection.sendmail(mail_from, recipient_emails, msg.as_string())
        print ("Sent email to {0}".format(', '.join(recipient_emails)))

    except smtplib.SMTPException, e:
        msg = '%r' % e
        print (msg)
        raise MailerException(msg)
    except:
        print "ERROR"
    finally:
        smtp_connection.quit()
#for line in harvester_run_log_tail:
#    print line
#print harvester_run_log_last_line

#print "CURRENT TIME"
#print current_time

try:
    mtime = os.path.getmtime(file_name)
except OSError:
    mtime = 0
last_modified = datetime.fromtimestamp(mtime)

#print "file last modified"
#print last_modified

print "Time difference"
time_difference_hours = (current_time - last_modified).total_seconds() / 3600
print time_difference_hours

if time_difference_hours > .00001:
    print "MORE"
    _ERRORS = True

if _ERRORS:
    msg = MIMEText(message_body.encode('utf-8'), 'plain', 'utf-8')
    _send_mail(mail_from, recipient_emails, msg)
