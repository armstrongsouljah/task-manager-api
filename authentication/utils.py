from django.contrib.auth import tokens as tk
from django.utils import six


class EmailVerificationTokenGenerator(tk.PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            six.text_type(user.id)+six.text_type(timestamp)
        )


email_verification_token = EmailVerificationTokenGenerator()