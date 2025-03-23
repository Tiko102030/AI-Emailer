import imaplib
import email
from email.header import decode_header
import time
import requests

# Zoho IMAP server settings
imap_server = "imap.zoho.com"
email_address = "tikosai@zohomail.com"
app_password = "jYEZPiqV3j8R"

def connect_to_mail():
    """Connect to Zoho IMAP server"""
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_address, app_password)
    mail.select("inbox")
    return mail

def fetch_latest_email(mail):
    """Fetch and print the latest email"""
    status, messages = mail.search(None, "UNSEEN")  # Fetch only new (unread) emails
    email_ids = messages[0].split()

    if email_ids:
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                print(f"\n📩 New Email Received:")
                print(f"Subject: {subject}")

                # Extract email content
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            print(f"Body:\n{body}")
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                    print(f"Body:\n{body}")

def listen_for_emails():
    """Continuously listen for new emails"""
    while True:
        try:
            mail = connect_to_mail()
            fetch_latest_email(mail)
            mail.logout()
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(1)  # Wait 1 second before checking again

# Start listening for emails
listen_for_emails()
