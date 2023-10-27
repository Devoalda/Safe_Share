import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email, from_email, from_password):
    """
    Send an email using Gmail's SMTP server.

    Args:
    - subject (str): Subject of the email.
    - body (str): Body content of the email.
    - to_email (str): Recipient email address.
    - from_email (str): Sender's Gmail email address.
    - from_password (str): Sender's Gmail password or app password.

    Returns:
    - bool: True if email was sent successfully, False otherwise.
    """

    # Constructing the email
    msg = MIMEText(body)
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.close()

        print('Email sent!')
        return True

    except Exception as e:
        print('Something went wrong:', e)
        return False

# Usage:
from_email = 'pureinc933@gmail.com'
from_password = 'dnmttxedjzlwjbdr'
to_email = 'xrando20@gmail.com'
subject = 'Test Subject'
body = 'This is the body of the email.'

send_email(subject, body, to_email, from_email, from_password)
