import base64
import random
import string
from collections import OrderedDict
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail


def sendemail(to='', from_="support@localhost", subject="User not recognized", body="Please email support at support@localhost"):
    """
    Sends email using sendgrid API.

    @param to str: receiver email.
    @param from_ str: sender email. [defaults to support_email]
    @param subject str: email subject.
    @param body str: email message content.

    """
    sg = sendgrid.SendGridAPIClient(apikey=app.config['SENDGRID_API_KEY'])
    from_email = Email(from_)
    to_email = Email(to)
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("Email sent..")
    print(response.status_code)
    print(response.body)
