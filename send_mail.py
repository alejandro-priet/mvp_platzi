import smtplib
from email.mime.text import MIMEText

def send_mail(customer, service, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '243b55b52bc0f9'
    password = '6df6159a49893a'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Dealer: {service}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'MVP Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())