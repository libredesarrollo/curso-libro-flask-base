from flask_mail import Message

# from my_app import app

def send_email(to,subject, template):
    msj = Message(
        subject=subject,
        recipients=[to],
        html= template,
        # sender=app.config['MAIL_DEFAULT_SENDER']
        )
    
    # mail.send(msj)