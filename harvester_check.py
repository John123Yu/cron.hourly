import os
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from email import Utils

file_name = '/var/log/harvester_run.log'
current_time = datetime.now()
recipient_emails = ['root@localhost']
mail_from = 'no-reply@data.gov'
harvester_errors = {'sqlalchemy.exc.OperationalError', 'Problems were found while connecting to the SOLR server'}
message_body = None

harvester_run_log = open(file_name, 'r').readlines()
harvester_run_log_tail = harvester_run_log[-15:-1]
#harvester_run_log_last_line = harvester_run_log[-2:-1][0]

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

for line in harvester_run_log_tail:
    if any(error in line for error in harvester_errors):
        message_body = line
        print line

#print harvester_run_log_last_line
try:
    mtime = os.path.getmtime(file_name)
except OSError:
    mtime = 0
last_modified = datetime.fromtimestamp(mtime)
time_difference_hours = (current_time - last_modified).total_seconds() / 3600
print "Time difference: " + str(time_difference_hours)

if time_difference_hours > 6:
    message_body = 'Harvest log has not been updated in 6 hours.'

if message_body:
    msg = MIMEText(message_body)
    msg['Subject'] = 'Harvest log error'
    #msg = MIMEText(message_body.encode('utf-8'), 'plain', 'utf-8')
    _send_mail(mail_from, recipient_emails, msg)
