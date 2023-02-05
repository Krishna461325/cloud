import json
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class SendEmail:
    def __init__(self, json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
        self.from_address = data["from"]
        self.to_address = data["to"]
        self.subject = data["subject"]
        self.body = data["body"]
        self.emailout = data.get("emailout", "")
        self.attachments = data.get("attachments", [])
        self.filename = data.get("filename", [])

    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = self.subject

        if self.emailout == "html":
            for filen in self.filename:
                with open(filen['filename'], "r") as f:
                    data = f.readlines()
                table = "<table>"
                for line in data:
                    table += "<tr>"
                    fields = line.strip().split(",")
                    for field in fields:
                        table += "<td>" + field + "</td>"
                    table += "</tr>"
                table += "</table>"
                body_part = MIMEText(table, "html")
                msg.attach(body_part)
        elif self.emailout == "attachments":
            body_part = MIMEText(self.body)
            msg.attach(body_part)
            for attachment in self.attachments:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(base64.b64decode(attachment["content"]))
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={attachment['filename']}")
                msg.attach(part)
        else:
            body_part = MIMEText(self.body)
            msg.attach(body_part)

        server = smtplib.SMTP('localhost')
        server.send_message(msg)
        server.quit()

'''
#usage
from send_email import SendEmail

json_file = "email_data.json"
email = SendEmail(json_file)
email.send_email()
'''



''' 
## error handling ###
import smtplib
import json
import os

class SendEmail:
    def __init__(self, json_file):
        self.json_file = json_file

        try:
            with open(json_file) as file:
                self.email_data = json.load(file)
        except FileNotFoundError:
            print("Error: JSON file not found")
            exit()
        except json.decoder.JSONDecodeError:
            print("Error: Invalid JSON file")
            exit()
    
    def send_email(self):
        try:
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.ehlo()
            smtp_server.starttls()
            
            from_address = self.email_data["from"]
            to_address = self.email_data["to"]
            subject = self.email_data["subject"]
            body = self.email_data["body"]
            emailout = self.email_data["emailout"]

            if emailout == "attachments":
                attachments = self.email_data["attachments"]

                msg = f"Subject: {subject}\n\n{body}"
                smtp_server.login(from_address, "your_password")
                smtp_server.sendmail(from_address, to_address, msg)
                for attachment in attachments:
                    filename = attachment["filename"]
                    try:
                        with open(filename, "rb") as file:
                            part = file.read()
                            smtp_server.send_message(from_address, to_address, part)
                    except FileNotFoundError:
                        print(f"Error: Attachment file not found: {filename}")
                        continue
            elif emailout == "html":
                filename = self.email_data["filename"]

                html = """\
                <html>
                <head></head>
                <body>
                <table border=1>
                """
                try:
                    with open(filename[0]["filename"], "r") as file:
                        lines = file.readlines()
                        for line in lines:
                            html += "<tr>"
                            for cell in line.split(","):
                                html += "<td>" + cell + "</td>"
                            html += "</tr>"
                except FileNotFoundError:
                    print(f"Error: File not found: {filename[0]['filename']}")
                    exit()

                html += """\
                </table>
                </body>
                </html>
                """
                message = f"""\
                Subject: {subject}

                {html}
                """
                smtp_server.login(from_address, "your_password")
                smtp_server.sendmail(from_address, to_address, message)
            else:
                print("Error: Invalid value for emailout")
                exit()

            smtp_server.quit()
            print("Email sent successfully")
        except smtplib.SMTPException as e:
            print("Error sending email:", e)


'''
