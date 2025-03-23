import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ----------------------------------- Email Credentials ----------------------------------- #
smtp_server = "smtp.zoho.com" # The address to the server I'm using, in this case, Microsoft office 
smtp_port = 587 
sender_email = "tikosai@zohomail.com" # My email address goes here
app_password = "jYEZPiqV3j8R" # App password for my email account (tikoai@outlook.com)

reciever_email = "tikhon102030@gmail.com" # Target email address, where the email will be sent to


# ------------------------------------- Email Content ------------------------------------- #
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = reciever_email
msg["Subject"] = "Test1 (Subject)" # Subject of sent email
msg.attach(MIMEText("Hello, this is the first test of sending the email through python. This is supposed to be the body, main text of the email. If you're reading this, it worked!", "plain"))


# ------------------------------------ Send the Email ------------------------------------ #
def send_email(sender_email, reciever_email):
    msg = MIMEMultipart()


try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, reciever_email, msg.as_string())
    print("Email sent!")
except Exception as e:
    print(f"Error: {e}")
