import smtplib
from email.message import EmailMessage
import os

def deliver_application(recipient_email: str, job_title: str, company: str, attachment_path: str, mock: bool = True):
    if mock:
        print(f"      [MOCK MODE] Email successfully sent to {recipient_email} for {job_title} role.")
        return

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_APP_PASSWORD")
    
    if not sender_email or not sender_password:
        raise ValueError("SMTP Credentials missing. Check your .env file.")

    msg = EmailMessage()
    msg['Subject'] = f"Application: {job_title} - Nikhil"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    body = f"Hello {company} Hiring Team,\n\nPlease find attached my tailored resume for the {job_title} position.\nI am excited about the opportunity to contribute to your engineering team.\n\nBest regards,\nNikhil"
    msg.set_content(body)

    try:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            
        msg.add_attachment(
            file_data, 
            maintype='application', 
            subtype='vnd.openxmlformats-officedocument.wordprocessingml.document', 
            filename=file_name
        )
    except Exception as e:
        raise IOError(f"Failed to attach file {attachment_path}: {e}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        raise PermissionError("SMTP Authentication failed. Ensure you are using an App Password.")