import requests
import datetime
import json
from dateutil.tz import gettz
from pprint import pprint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time

def runVaccineSearch():

    print(datetime.datetime.now())

    date_today = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime("%d-%m-%Y")
    date_7thd = (datetime.datetime.now(tz=gettz('Asia/Kolkata')) + datetime.timedelta(days=7)).strftime("%d-%m-%Y")

    url1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=505&date=" + date_today
    url2 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=506&date=" + date_7thd

    try:
        r1 = requests.get(url1)
        data1 = json.loads(r1.text)
    except Exception as e:
        sendEmail(e)
        print("Error in Vaccine Search")
    message1 = ""

    try:
        r2 = requests.get(url2)
        data2 = json.loads(r2.text)
    except Exception as e:
        sendEmail(e)
        print("Error in Vaccine Search")
    message2 = ""

    if('centers' in data1.keys()):
        for center in data1['centers']:
            if('sessions' in center.keys()):
                for session in center['sessions']:
                    if(session['min_age_limit'] != 18):
                        continue
                    elif(session['available_capacity'] == 0):
                        continue
                    else:
                        message1 = message1 + "center_name - " + center['name'] + ", " + "district_name - " + center['district_name'] + ", " + "date - " + str(session['date']) + ", " + "available_capacity - " + str(session['available_capacity']) + ", " + "min_age_limit - " + str(session['min_age_limit']) + ", " + "vaccine_name - " + session['vaccine'] + "<br><br>"

    if('centers' in data2.keys()):
        for center in data2['centers']:
            if('sessions' in center.keys()):
                for session in center['sessions']:
                    if(session['min_age_limit'] != 18):
                        continue
                    elif(session['available_capacity'] == 0):
                        continue
                    else:
                        message2 = message2 + "center_name - " + center['name'] + ", " + "district_name - " + center['district_name'] + ", " + "date - " + str(session['date']) + ", " + "available_capacity - " + str(session['available_capacity']) + ", " + "min_age_limit - " + str(session['min_age_limit']) + ", " + "vaccine_name - " + session['vaccine'] + "<br>>br>"

    message = message1 + message2
    if(len(message) != 0):
        sendEmail(message1 + message2)
    else:
        print("No Vaccine Found")


def sendEmail(message):

    try:
        mail_content = "<p><strong>Vaccine Availability - </strong></p><br>"
        mail_content = mail_content + message

        sender_address = "<EMail>"
        sender_pass = "<Password>"

        to_email = "<Email1>"
        cc_email = "<Email2>"
        rcpt = to_email.split(",") + cc_email.split(",")

        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = to_email
        message['Cc'] = cc_email
        message['Subject'] = "Covid Vaccine Found"

        message.attach(MIMEText(mail_content, 'html'))

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, rcpt, text)
        session.quit()

        print("Mail Sent")

    except Exception as e:

        print(e)
        print("Error in Sending E-Mail")

schedule.every(300).seconds.do(runVaccineSearch)

while True:
    schedule.run_pending()
    time.sleep(100)
