from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def send_email(data):
    email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    email.send()


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (str(user.is_active) + str(user.pk) + str(timestamp))


token_generator = AppTokenGenerator()