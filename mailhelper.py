import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import Encoders
import os

from settings import GMAIL_USER, GMAIL_PWD, NOTIFY_EMAIL

def mail(to, subject, text, attach=None, image=None):
   msg = MIMEMultipart()
   msg['From'] = GMAIL_USER
   msg['To'] = to
   msg['Subject'] = subject
   msg.attach(MIMEText(text))
   if attach:
      part = MIMEBase('application', 'octet-stream')
      with open(attach, 'rb') as f:
        part.set_payload(f.read())
      Encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
      msg.attach(part)
   if image:
       with open(image, 'rb') as f:
         part = MIMEImage(f.read(), name=os.path.basename(image))
       msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(GMAIL_USER, GMAIL_PWD)
   mailServer.sendmail(GMAIL_USER, to, msg.as_string())
   mailServer.close()

def main():
    mail(NOTIFY_EMAIL, "Test Message", "This was a test")

if __name__ == "__main__":
    main()
