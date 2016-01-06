# -*- coding:utf-8 -*-
import imp
import sys
import json
imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的
from pymongo import MongoClient

import urllib
import urllib2
import re

def send_email( text ):
        import smtplib
        from email import encoders
        from base64 import b64encode
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        gmail_user = "email"
        gmail_pwd = "password"
        FROM = 'email'
        TO = ['email'] #must be a list
        SUBJECT = "爬菜"

        # Prepare actual message
        msg = MIMEMultipart('alternative')
        # 注意包含了非ASCII字符，需要使用unicode
        msg['Subject'] = SUBJECT
        msg['From'] = FROM
        msg['To'] = ', '.join(TO)
        part = MIMEText(text, 'plain', 'utf-8')
        msg.attach(part)

        try:
            #server = smtplib.SMTP(SERVER)
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, msg.as_string())
            #server.quit()
            server.close()
            print 'successfully sent the mail'
        except:
            print "failed to send mail"

client = MongoClient()
db = client.pacai

mailText = ""
from random import randint
for num in range(1, 5):
    indexMenu = randint(0, 386)
    result = db.test.find({"index" : indexMenu})

    if result:
        ingredient = "准备材料： "
        menu = "菜名: "
        cookbook = "做法： "
        for key, value in result[0].iteritems():
            if key == "ingredient":
                ingredient = ingredient + value + '\n'
            if key == "menu":
                menu = menu + value + '\n'
            if key == "cookbook":
                cookbook = cookbook + value + '\n'
        mailText = mailText + menu + ingredient + cookbook + '\n'
print mailText
send_email(mailText)