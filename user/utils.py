from django.core.mail import EmailMessage


class Util:
    """Send message"""

    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()
