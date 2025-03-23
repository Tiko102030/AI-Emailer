import imaplib
import email
from email.header import decode_header

# IMAP settings for Zoho Mail
imap_server = "imap.zoho.com"
imap_port = 993
email_address = "tikosai@zoho.com"
app_password = "jYEZPiqV3j8R"

# Connect to Zoho IMAP
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(email_address, app_password)
mail.select("inbox")  # Select the inbox

# Fetch the latest email
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

if email_ids:
    latest_email_id = email_ids[-1]  # Get the last email
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg["Subject"])[0]

            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            print(f"Subject: {subject}")

            # Extract email content
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        print(f"Body:\n{body}")
            else:
                body = msg.get_payload(decode=True).decode()
                print(f"Body:\n{body}")

# Close connection
mail.logout()
