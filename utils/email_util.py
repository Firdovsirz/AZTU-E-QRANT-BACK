import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587 
SMTP_USER = "firdovsirz@gmail.com"
SMTP_PASSWORD = "txjf wgkx mqdi fban"

def send_email(subject: str, recipient: str, html_content: str, text_content: str = None):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_USER
        msg['To'] = recipient
        msg['Subject'] = subject

        if text_content:
            msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, recipient, msg.as_string())
            print(f"[DEBUG] Email sent to {recipient}")
    except Exception as e:
        print(f"[ERROR] Failed to send email to {recipient}: {e}")