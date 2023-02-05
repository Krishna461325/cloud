import smtplib
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class Sendemail:
    def __init__(self, data):
        self.data = data
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

    def send(self):
        self.server.ehlo()
        self.server.starttls()
        self.server.login('sender@example.com', 'password')
        self.send_email()
        self.server.quit()

    def send_email(self):
        from_email = self.data.get('from')
        to_email = self.data.get('to')
        subject = self.data.get('subject')
        body = self.data.get('body')
        emailout = self.data.get('emailout')
        attachments = self.data.get('attachments')
        source = self.data.get('source')

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body))

        if emailout == 'attachments':
            for attachment in attachments:
                filename = attachment.get('filename')
                with open(filename, "rb") as f:
                    part = MIMEApplication(f.read(), Name=filename)
                part['Content-Disposition'] = f'attachment; filename="{filename}"'
                msg.attach(part)

        if emailout == 'html':
            if source[0].get('file'):
                filename = source[0].get('file')
                with open(filename, 'r') as f:
                    html = f.read()
                msg.attach(MIMEText(html, 'html'))
            elif source[0].get('dataframe'):
                df = source[0].get('dataframe')
                html = df.to_html()
                msg.attach(MIMEText(html, 'html'))

        self.server.sendmail(from_email, to_email, msg.as_string())

if __name__ == "__main__":
    data = { 
        "from": "sender@example.com", 
        "to": "receiver@example.com", 
        "subject": "Example subject", 
        "body": "This is a sample email with HTML formatting",
    }
    email = Sendemail(data)
    email.send()
