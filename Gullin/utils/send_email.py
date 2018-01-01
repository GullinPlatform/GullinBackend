from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.conf import settings


def send_email(receiver_list, subject, template_name, ctx):
	"""
	:param receiver_list: The list of receivers email with send to
	:param subject: Email subject
	:param template_name: Email template using
	:param ctx: Email context
	:return: None
	"""
	email_message = render_to_string('email/%s.html' % template_name, ctx)

	email = EmailMessage(subject, email_message, settings.EMAIL_SEND_FROM, receiver_list)
	email.content_subtype = 'html'
	email.send()

	return
