from celery import shared_task
from django.contrib.auth import tokens as tk
from django.core.mail import EmailMessage


class EmailVerificationTokenGenerator(tk.PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.id) + str(timestamp)


email_verification_token = EmailVerificationTokenGenerator()


@shared_task()
def send_gen_email(subject=None, email_body=None, sender_mail=None, receipients: list = []):
    """Utility for send email accros the app."""
    message = EmailMessage(
        subject=subject, body=email_body, from_email=sender_mail, to=receipients
    )
    return message.send(fail_silently=False)
