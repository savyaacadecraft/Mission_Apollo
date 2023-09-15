from requests import get, post
import smtplib
from email.mime.text import MIMEText
from email import message_from_bytes, message_from_string
import imaplib
from time import sleep
from traceback import print_tb

def sendMail(recipient):
    try:
        host = "smtp.gmail.com"
        port = 465

        sender = "mail.anirudh1997@gmail.com"
        password = "qqcwppbbajoxebpe"

        subject = "Server Stopped"
        msg = "LinkedIn Atlas Project crashed.\n\nPlease restart Immediately....."
        
        msg = MIMEText(msg)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        smtp_server = smtplib.SMTP_SSL(host, port)
        smtp_server.login(sender, password)

        smtp_server.sendmail(from_addr=sender, to_addrs=recipient, msg=msg.as_string())

        smtp_server.quit()
        print("Mail Sent.....")

    except Exception as E:
        print("Exception: ", print_tb(E.__traceback__))


def alive_cheker():
    while True:
        try:
            url = 'https://emailfinder.in/'
            response = get(url)
            print(response.status_code)
            if response.status_code == 200:
                print("...")
            else:
                print("###")
                sendMail("mailme.savya@gmail.com")
                sendMail("developer@crazyforstudy.com")
                sendMail("developer@acadecraft.com")

            sleep(30)
        except Exception as e:
            print(e)

if __name__=='__main__':
    alive_cheker()


