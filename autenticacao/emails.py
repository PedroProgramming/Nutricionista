from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings



def send_email(path_template: str, assunto: str, para: list, **kwargs) -> dict:

    html = render_to_string(path_template, kwargs)
    text = strip_tags(html)

    email = EmailMultiAlternatives(assunto, text, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html, "text/html")
    email.send()
    return {'status': 1}