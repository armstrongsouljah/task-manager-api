from celery import shared_task
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
# from django.shortcuts import redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from decouple import config
import logging 
from celery.utils.log import get_task_logger
from rest_framework.pagination import PageNumberPagination

log = logging.getLogger(__name__)
logger = get_task_logger(__name__)


DEFAULT_FROM_EMAIL= config('DEFAULT_FROM_EMAIL')

def generate_verification_url(user, request):
    uuid = urlsafe_base64_encode(
            force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    email_verification_url = reverse(
            'user-auth:email-verification', args=[uuid, token])
    url = request.build_absolute_uri(email_verification_url)
    username = user.email.split("@")[0]
    return {
        'url': url,
        'username': username,
        'email': user.email
    }



@shared_task()
def send_activation_email(url=None,username=None,email=None):
    # user = User.objects.get(pk=user_id)
    # uuid = urlsafe_base64_encode(
    #         force_bytes(user.pk)).decode()
    # token = email_verification_token.make_token(user)
    subject = "Email Verification For Your Todos"
    # email_verification_url = reverse(
    #         'authentication:email-verification', args=[uuid, token])
    # url = request.build_absolute_uri(email_verification_url)

    # username = user.email.split("@")[0]
    context = {'username': username,
                   'url': url, 'app_name': "Todos Manager"}

    message_string = render_to_string('email.html', context,)
    reciever_email = email
    default_receiver = DEFAULT_FROM_EMAIL
    sender_email = DEFAULT_FROM_EMAIL
    print('Email....details....')
    print(subject, message_string, default_receiver, reciever_email)

    try:
        email = EmailMessage(
            subject=subject,
            body=message_string,
            from_email=sender_email,
            to=[reciever_email,]
        )
        email.send(fail_silently=False)
        logger.info("Email sent successfully..")
        return True
    except Exception as e:
        logger.info("Email sending failed..")
        logger.error(e)
        return False

    # email = EmailMessage(
    #     subject=subject,
    #     body=message_string,
    #     from_email=DEFAULT_FROM_EMAIL,
    #     to=[reciever_email,default_receiver])
    # logger.info("Email sending email.....")
    
    # try:
    #     email.send()
    #     # send_mail(subject,message_string,DEFAULT_FROM_EMAIL,[reciever_email,default_receiver])
    #     logger.info("Email sent successfully")
    #     return True
    # except Exception as e:
    #     msg = f"Error sending activation email, {e}"
    #     logger.info(msg)
    #     return False





class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            six.text_type(user.id)+six.text_type(timestamp)
        )


email_verification_token = EmailVerificationTokenGenerator()




class CustomPagination(PageNumberPagination):
    """
    Class to configure pagination parameters
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15
    page_query_param = 'page'