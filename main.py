import smtplib
import imaplib
import json
import requests
import time
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header

# ----------------------------------- Email Credentials ----------------------------------- #
imap_server = "imap.zoho.com"
smtp_server = "smtp.zoho.com" 
smtp_port = 587 
sender_email = "tikosai@zohomail.com" 
app_password = "jYEZPiqV3j8R" 

reciever_email = "tikhon102030@gmail.com" 


def connect_to_mail():
    """Connect to Zoho IMAP server"""
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(sender_email, app_password)
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
                    
                from_address = email.utils.parseaddr(msg["From"])[1]

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

                get_ollama_answer(body, from_address)
                mail.store(latest_email_id, '+FLAGS', '\\Seen')

def listen_for_emails():
    """Continuously listen for new emails"""
    while True:
        try:
            mail = connect_to_mail()
            fetch_latest_email(mail)
            mail.logout()
        except Exception as e:
            print(f"Error listening for emails: {e}")
        
        time.sleep(1)  # Wait 1 second before checking again




def send_email(sender_email, reciever_email, subject, email_body):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = reciever_email
    msg["Subject"] = subject
    msg.attach(MIMEText(email_body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, reciever_email, msg.as_string())
        print("Email sent!")
    except Exception as e:
        print(f"Error sending email: {e}")



def query_ollama(prompt, model="llama3.1:8b"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    else:
        return f"Ollama Error: {response.status_code}, {response.text}"

def get_ollama_answer(question, sender_email):
    ollama_answer = query_ollama(question)
    print(f"Ollama answer: {ollama_answer}")
    send_email("tikosai@zohomail.com", sender_email, "AI Answer", ollama_answer)



listen_for_emails()