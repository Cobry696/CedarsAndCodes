from email.message import EmailMessage
import ssl
import smtplib

def send_email(email_sender: str, sender_password: str, to_email: str, body: str, subject: str):

    """
    Basic function that sends an email
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = to_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, sender_password)
            smtp.sendmail(email_sender, to_email, em.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        pass
        print(f"Failed to send email: {e}")