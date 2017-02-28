#!/usr/bin/python

import smtplib
import sys
import os
import smtplib       # this invokes the secure SMTP protocol (port 465, uses SSL)
from email.MIMEText import MIMEText

DEBUG = False
test_recipients = []
SMTPserver = 'mail.rpi.edu'
subject="CS 1 Final Grade Feedback"
text_subtype = 'plain'
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
filename = sys.argv[3]
sender = USERNAME + '@rpi.edu'
            
def sendMsg(conn,receiver,content):
    try:
        if DEBUG:
            destination = test_recipients
        else:
            destination = [receiver]    
        msg = MIMEText(content, text_subtype)
        msg['Subject']=       subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all
        conn.sendmail(sender, destination, msg.as_string())

    except Exception, exc:
        sys.exit( "mail failed; %s" % str(exc) ) # give a error message

def gen_message(last,first,final,final_curved,test_avg,cum_avg,letter,username):
    result = ''
    if DEBUG:
        result = '%s@rpi.edu' % username
    result += '\n' + last + ', ' + first
    result += '\n' + 'Final exam (out of 120): %s' % final
    result += '\n' + 'Final exam curved (out of 120): %s' % final_curved
    result += '\n' + 'Test average: %s' % test_avg
    result += '\n' + 'Cumulative average: %s' % cum_avg
    result += '\n' + 'Letter grade: %s' % letter
    result += '\n'  
    return result

with open(filename) as fp:
    conn = smtplib.SMTP('%s:%s'%(SMTPserver,587))
    conn.ehlo()
    conn.starttls()
    conn.set_debuglevel(True)
    conn.login(USERNAME, PASSWORD)
    for lineno,line in enumerate(fp.readline().split('\r')):
        if lineno > 0: 
            elems = line.split(',')
            last_name = elems[1]
            first_name = elems[2]
            final_grade = elems[3]
            final_curved = elems[4]
            test_avg = elems[5]
            cum_avg = elems[6]
            letter_grade = elems[7]
            username = elems[0] 
            msg = gen_message(last_name,first_name,final_grade,final_curved,test_avg,cum_avg,letter_grade,username)
            sendMsg(conn,username+'@rpi.edu',msg)   
    conn.close()









